# AI Usage Summary

During this assignment, the core **thinking process and logical direction** were strictly mine. I utilized Antigravity and Codex specifically for script execution, coding, and mathematical validation. 

### Where it helped

#### Part A (Tokenizer Audit & Analysis):
- **Initial Scan & Bug Finding:** I directed the AI to do a first scan of the intern's `fertility.py` script. The AI successfully spotted the code bugs (lowercasing and macro-averaging) and isolated their mathematical impact.
- **Environment & Scripting:** The AI wrote the execution scripts to fetch the FLORES and IN22 datasets and automated the `a3_analysis.ipynb` evaluation loop across the 4 tokenizers based on my conceptual shift to "tokens per sentence".

#### Part B (Capacity Reconciliation):
- **Generating the Math & Diagnostics:** I was initially unsure of the exact steps to calculate the KV-cache bytes per token or the maximum concurrent sequences. I relied on AI agents to derive the formulas and identify the KV-cache thrashing mechanism.
- **Cross-Model Validation:** Because I wasn't confident in the initial output, I ran the Part B scenario through several different frontier models. I analyzed and compared their answers, and only finalized the calculations once I was satisfied with the consistency and logic of the results.
#### Part C & Documentation:
- **Decision Memo:** I personally completed the core analysis for all three proposed paths (A, B, and C) and independently arrived at the final solution. I then utilized the AI to help ideate, document, and neatly format my findings and results into the final memo structure.
- **Lab Notebook Compilation:** The AI formatted my chronological journey, hypotheses, and dead-ends into a readable structure for the final notebook.

### Where it misled me or required overrides

- **The OPUS Dataset Hallucination:** The AI initially recommended the OPUS-100 dataset as a conversational corpus. I had to scrap this recommendation because OPUS-100 is largely bilingual and heavily polluted with religious/software text rather than casual dialogue.
- **Lack of Evidence Grounding:** The AI frequently attempted to state conclusions without providing the underlying mathematical or empirical proofs. I had to explicitly force it to ground its results in hard evidence and step-by-step derivations (especially in the Part B capacity math).
- **Context Bleed Between Tasks:** The AI struggled to treat the assignment as three distinct, independent modules. It often mixed contexts from Part A, Part B, and Part C together, requiring me to manually intervene and enforce strict boundaries between the sub-problems.
