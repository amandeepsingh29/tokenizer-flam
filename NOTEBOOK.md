# Lab Notebook

This notebook serves as a chronological record of the hypothesis, experimentation, and analysis process across all parts of the assignment.

## Part A: Tokenizer Audit Journey

### A1: Building the Multilingual Eval Corpus
**Objective:** Assemble a robust n-way parallel evaluation corpus across 4 languages (English, Hindi, Tamil, Kannada).
**Exploration & Dead Ends:** 
- Initially explored the OPUS-100 dataset. *REJECTED* because it is largely bilingual pairs rather than strictly n-way parallel across our target languages.
- **Final Corpus Selection:** Settled on building a custom dataset combining FLORES-200 (for formal/encyclopedic text) and IN22-Gen/IN22-Conv (for news and conversational data).
- **Result:** Successfully extracted 3,539 strictly parallel sentences per language. This provides a strong baseline but comes with a caveat: it cannot tell us how tokenizers perform on highly informal, noisy user data (like code-mixed Hinglish slang).

### A2: Script & Metric Audit (Isolating the Flaws)
**Hypothesis 1 (Lowercasing Bug):** The intern's code lowercases all text. I suspect this artificially inflates the English vs. Hindi gap because the `gpt2` tokenizer is cased and struggles with lowercased proper nouns.
**Experiment:** I ran `fertility.py` on the sample corpus. It gave me the intern's 5.89x number. I then modified the script to isolate the lowercase bug by keeping casing intact.
**Result (Surprise!):** Fixing the bug dropped English fertility slightly from 1.27 to 1.23, which actually *widened* the gap to 6.06x! The original bug was slightly masking the true difference.

**Hypothesis 2 (Macro-average Bug):** Averaging per-line ratios distorts the metric by heavily weighting very short sentences.
**Experiment:** I wrote a new function to sum all tokens divided by all words (micro-average).
**Result:** English went to 1.25, Hindi to 7.40. The gap shifted to 5.91x. Another minor distortion isolated, but clearly not the root cause.

**Hypothesis 3 (Conceptual Flaw - The Denominator):** Words are a terrible denominator for cross-lingual comparison because semantic density per word varies wildly by grammar (e.g., Hindi's postpositions).
**Experiment:** Switched the denominator to "Tokens per Sentence", holding semantic payload constant across parallel data.
**Result:** The baseline GPT-2 ratio dropped heavily to 4.78x on the sample corpus. This proved that "Tokens per Word" was the core conceptual failure.

### A3: Corrected Analysis
**Objective:** Run the corrected metric (Tokens per Sentence) across the entire ~14k sentence corpus using multiple tokenizers.
**Experiment:** Developed an automated evaluation script (`A2_A3_analysis.ipynb`) to test `gpt2`, `gpt-4o`, `llama-3`, and `xlm-roberta`.
**Result:** XLM-Roberta emerged as the absolute best for Indic languages, dropping the English-to-Hindi multiplier from 7.41x (GPT-2) down to just 1.21x - 1.25x.

### A4: Recommendation Memo (Overview)
**Conclusion:** We do not need a separate routing architecture for Indic languages.
**Recommendation:** Upgrade the core tokenizer to XLM-Roberta or GPT-4o (`o200k_base`), which naturally compresses Indic text. 
**Production Monitor:** To ensure real-world noisy data doesn't break this assumption, we must monitor the `average_generated_tokens_per_request` segmented by `detected_language` in production.

---

## Part B: Capacity & Throughput Reconciliation

### B1: Capacity Math (KV-Cache Budget)
**Hypothesis:** Can we mathematically predict the maximum concurrent requests from the hardware specs alone?
**Experiment:** Based on the model spec (28 layers, 8 KV heads, 128 dim, fp16), I calculated the KV-cache requirement: `2 * 28 * 8 * 128 * 2 = 114,688 bytes/token`. I subtracted the model weights and overhead from the 24GB VRAM (leaving 12.08 GB for KV cache).
**Result:** 12.08 GB / 114,688 bytes = 105,329 total tokens. Divided by 4096-token sequences = **25.71 max concurrent sequences**.
**Validation:** I cross-referenced the log. At batch 24, `kv_cache_util` is 0.93. My math predicted 24 / 25.71 = 93.3%. The math flawlessly matches the telemetry!

### B2: The Throughput Anomaly
**Observation:** Throughput crashed at batch 32 and 48 in the long-context sweep (dropping from 1607 tok/s to 1384 tok/s).
**Diagnosis:** The `preempted_seqs` column spiked from 0 (batch 24) to 7 (batch 32). This proves the system hit the hard 25-sequence physical limit I calculated in B1 and started trashing the KV cache. 
**Recommendation:** Add a `--max-num-seqs 24` limit to the serving engine configuration.

### B3: The "Longer Prompt" Illusion
**Observation:** The intern claimed long prompts give better throughput (3200 tok/s at batch 48).
**Hypothesis:** `reported_tok_s` is a blended metric that mixes ultra-fast parallel prefill with slow sequential decoding.
**Experiment:** I calculated pure decode speed ("goodput") using macro-level wall-clock time: `(24 requests * 512 tokens) / 61.16s = 200.9 tok/s`.
**Validation:** I de-blended the metric mathematically: `1607.4 * (512 / 4096) = 200.9 tok/s`.
**Result:** The math perfectly converges. The intern's metric was severely bloated by the prefill phase, leading to a catastrophic capacity miscalculation.

### B4: Serving Metric Confirmation
**Recommendation:** If you are an engineer looking at a live production dashboard, and you see throughput drop, how do you mathematically prove it's because of KV-cache thrashing and not just a bad network connection or a CPU bottleneck?

You look for a counter that specifically tracks those "pauses". In standard serving engines like vLLM, this Prometheus metric is usually called something like `vllm:num_preemptions` or `swap_outs`.

**What you expect to see:**
If your math in B1 is correct (and it is), you know the limit is 25. Therefore, you would expect this `num_preemptions` metric on your dashboard to read exactly 0 when the batch size is 4, 8, 16, or 24. There is plenty of memory, so no requests get paused.

However, the exact millisecond the batch size hits 32, you would expect that metric to violently spike above zero. Seeing that specific metric spike at that exact batch size is the absolute, undeniable proof that your B1 math and B2 theory are correct in a live environment.

---

## Part C: Decision Memo (Casualization)
**Objective:** Inject a casual tone in six Indic languages under strict compute and time constraints.
**Exploration & Dead Ends:**
- Path B (≤1B inference-time rewriter): *REJECTED.* Adds serving complexity, TTFT latency, and presents a massive risk of dialect failure and "English fallback" since we lack native reviewers for 4 of the 6 languages.
- Path C (Prompting): *Fallback.* Fast and free, but highly susceptible to losing instruction priority in long contexts.
**Final Recommendation (Path A):** We will utilize our A100 window to run LoRA SFT on locally generated casualized pairs. Because we only have a Hindi/Kannada reviewer, we will implement a strict kill-criterion: we gate the rollout on a manual A/B review on Day 5. If it fails, we fall back to prompt engineering.
