# Part B: Capacity Reconciliation

## B1: Capacity Math

### a) KV-Cache Bytes per Token
Based on the `FLM-4B-Instruct` model spec:
- Layers: 28
- KV Heads (GQA): 8
- Head Dimension: 128
- Precision: fp16 (2 bytes per element)
- Stored vectors: 2 (Key and Value)

**Calculation:**
`2 vectors × 28 layers × 8 heads × 128 dimension × 2 bytes = 114,688 bytes per token`

### b) Max Concurrent 4096-token Sequences
To align exactly with the KV utilization reported by the internal vLLM/serving engine, we use decimal gigabytes ($1 \text{ GB} = 10^9 \text{ bytes}$):

* **Total VRAM:** 24 GB = 24,000,000,000 bytes
* **Serving Engine Allocation:** $24\text{e}9 \times 0.92 = 22,080,000,000$ bytes
* **Model Weights:** $4.2 \times 10^9 \text{ params} \times 2 \text{ bytes} = 8,400,000,000$ bytes
* **Non-KV Overhead:** 1,600,000,000 bytes
* **Remaining KV Cache Budget:** $22.08\text{e}9 - 8.4\text{e}9 - 1.6\text{e}9 =$ **12,080,000,000 bytes**

**Max Capacity:**
* Total Tokens = $12,080,000,000 \text{ bytes} / 114,688 \text{ bytes/token} = 105,329 \text{ tokens}$
* Max 4096-token Sequences = $105,329 / 4096 = 25.71$ sequences

**Log Verification:**
My arithmetic dictates that the hard limit is **25 concurrent requests**. The log completely confirms this: at batch size 24, the `kv_cache_util` is listed as exactly `0.93`. Our math predicts $24 / 25.71 = 93.3\%$. The math flawlessly matches the telemetry.

---

## B2: Throughput Anomaly (Long-Context Sweep)

**The Anomaly:**
In a standard serving scenario, throughput (`reported_tok_s`) should increase or plateau as batch size increases. In the long-context sweep (prompt=3584), throughput steadily climbs from batch 4 up to batch 24 (peaking at 1607 tok/s). However, at batch 32, throughput violently *crashes* down to 1384 tok/s, and further drops to 1298 tok/s at batch 48.

**The Mechanism:**
This is caused by catastrophic **KV cache thrashing**. Our B1 math proved the GPU can only hold ~25 concurrent 4096-token sequences. When batches of 32 and 48 are submitted, the engine hits a hard Out-Of-Memory wall for the KV cache. The scheduler is forced to evict/preempt active requests to make room for others, pausing generation and recomputing prefill states. We can prove this by looking at the `preempted_seqs` column, which spikes from 0 (at batch 24) to 7 (at batch 32) and 23 (at batch 48).

**Proposed Deployment Change:**
Limit the maximum concurrent sequences at the serving engine level (e.g., `--max-num-seqs 24` in vLLM).
* **Predicted Quantitative Effect:** By artificially capping concurrency below the physical 25-sequence limit, excess requests (like the extra 8 in batch 32) will queue safely instead of causing cache thrashing. The throughput will stabilize  the peak ~1600 tand plateau nearok/s instead of crashing into the 1200s.

---

## B3: The "Longer Prompt" Illusion & True Goodput

**The Misreading:**
Section 2 of the report concludes that longer prompts yield better throughput and that batch 48 will reach ~3200 tok/s. This stems from a very common, yet critical, misreading of the `reported_tok_s` column. 

That specific column blends two completely different computational phases: **prefill** (reading the prompt) and **decode** (generating the response). Because reading the prompt happens massively in parallel while generating the response is a slow sequential process, dumping a massive 3,584-token prompt into the engine makes the blended `reported_tok_s` number artificially skyrocket. The GPU isn't actually writing words any faster; the metric is simply padded with prefill tokens. 

**Deriving the Honest Goodput (Batch-24 Long-Prompt):**
To measure what the end-user actually experiences, we need to extract the pure generation throughput ("goodput"). We can mathematically prove the true generation speed using two independent methods from the `bench_log.csv` data:

1. **Method 1: Macro Definition (Total Output Tokens / Wall Clock Time)**
   We generated 512 tokens for 24 requests in 61.16 seconds.
   `Goodput = (24 requests × 512 tokens) / 61.16 seconds` = **200.9 tok/s**

2. **Method 2: De-blending the Reported Metric**
   The `reported_tok_s` metric (1607.4) represents `(Total Tokens) / Time`. We can isolate the generation speed by multiplying it by the ratio of generated tokens to total tokens (512 / 4096).
   `Goodput = 1607.4 × (512 / 4096)` = **200.9 tok/s**

Both proofs lock in at the exact same number: the actual generation speed is ~201 tok/s, an 87% drop from the reported 1607 tok/s. 

**What the report should have said:**
*"While extending prompt length artificially inflates our blended tokens/sec metric due to parallel prefill, our true generation goodput peaks at ~201 tok/s. Furthermore, we cannot assume linear scaling to batch 48. As proven by our capacity math, our L4 GPUs hit a hard KV-cache ceiling at 25 concurrent long-context sequences, meaning any batch larger than 25 will trigger cache eviction and actively degrade throughput."*

---

## B4: Single Serving Metric Confirmation

To definitively confirm that KV cache exhaustion and thrashing is the root cause of the B2 anomaly in production, I would pull the **`vllm:num_preemptions`** (or `vllm:swap_outs`) counter from the serving stack's Prometheus endpoint. I would expect this metric to remain perfectly flat at **0** for all batch sizes up to 24, and then suddenly spike to a non-zero, rapidly increasing rate during the batch 32 and batch 48 load tests (directly mirroring the exact 7 and 23 preemptions observed in the CSV log).
