# AI Usage Summary

I used Antigravity and Codex extensively during this assignment to accelerate scripting, validate mathematical models, and structure the final memos. Below is a detailed breakdown of where AI was utilized and where I had to override it.

### Where it helped

#### Part A (Tokenizer Audit & Analysis):
- **Environment & Scripting:** The AI set up the base environment, wrote the Python scripts to fetch the FLORES and IN22 datasets from HuggingFace, and automated the `A2_A3_analysis.ipynb` evaluation loop across the 4 tokenizers.
- **Spotting Code Bugs:** The AI instantly caught the macro-averaging and lowercase bugs in the intern's script and mathematically isolated their impact for the `a2_audit_observations.md`.
- **Conceptual Framing:** The AI helped articulate the precise linguistic reason why "tokens per sentence" is the mathematically rigorous denominator compared to "tokens per word."

#### Part B (Capacity Reconciliation):
- **Math Validation:** I used the AI to double-check my arithmetic for the KV-cache budget (114,688 bytes/token -> 25 concurrent sequences). It confirmed that the math perfectly aligned with the 0.93 `kv_cache_util` in the log.
- **Diagnostics:** The AI helped explain the underlying systems engineering mechanism (KV cache thrashing and swap-outs) that caused the throughput crash at batch 32, as well as the blended metric illusion (prefill vs. decode).

#### Part C & Documentation:
- **Decision Memo:** The AI helped structure the Decision Memo (Part C), particularly formatting the success metrics into a clean table and ensuring the back-of-the-envelope reviewer math (1,800 pairs) mapped correctly to the time constraint.
- **Lab Notebook Compilation:** The AI assisted in compiling the final `NOTEBOOK.md`, formatting the chronological journey, hypotheses, and dead-ends into a readable structure based on my scratchpad notes.

### Where it misled me or required overrides

- **The OPUS Dataset Hallucination (Part A):** The AI initially recommended the OPUS-100 dataset as a conversational corpus. I had to scrap this recommendation because OPUS-100 is largely bilingual (not strictly n-way parallel) and heavily polluted with religious/software text rather than casual dialogue.
- **Missing Required Memo Components (Part A):** In early drafts of the `a4_memo.md`, the AI fixated entirely on the data tables and completely forgot to include the routing recommendation, the biggest caveat, and the production metric. I had to explicitly prompt it to append these critical sections.
- **Context Loss:** When generating the initial capacity math, the AI had a minor hallucination regarding the `max-num-seqs` configuration and required manual correction to align exactly with the physical 25-sequence limit.
