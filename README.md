# Tokenizer & Capacity Audit

This repository contains the complete technical deliverables for the Tokenizer Audit, Capacity Reconciliation, and Tone Casualization project.

## 📂 Directory Structure & Deliverables

The submission is organized strictly according to the assignment requirements:

```text
tokenizer-flam/
├── NOTEBOOK.md            # A comprehensive chronological log of hypotheses, experiments, and validations
├── AI_USAGE.md            # Detailed breakdown of my workflow and AI usage boundaries
├── partA/                 # Tokenizer Audit & Analysis
│   ├── a1_corpus.md           # Documentation of corpus construction and caveats
│   ├── a2_script_audit.md     # Identification and quantification of logic/math bugs in the intern's script
│   ├── a3_analysis.ipynb      # The corrected Jupyter notebook evaluating 4 tokenizers
│   ├── a4_recommendation.md   # The final routing recommendation and production metric memo
│   ├── prepare_corpus_flores.py # Script to download the FLORES-200 subset
│   └── prepare_corpus_in22.py   # Script to download the IN22 subset
├── partB/                 # Capacity Reconciliation
│   └── b_capacity.md          # KV-cache math, log validation, and the throughput anomaly diagnosis
└── partC/                 # Tone Casualization Strategy
    └── memo.md                # Decision memo proposing the LoRA SFT approach with strict kill criteria
```

## 🚀 How to Reproduce Part A

To run the tokenizer evaluation locally:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Download the Evaluation Corpus:**
   Because IN22 is a gated dataset on Hugging Face, you must accept the terms on HF and set your token:
   ```bash
   export HF_TOKEN="your_huggingface_token"
   python partA/prepare_corpus_flores.py
   python partA/prepare_corpus_in22.py
   ```
3. **Run the Analysis:**
   Open and execute all cells in `partA/a3_analysis.ipynb`.

## 📊 High-Level Findings

* **Part A:** The intern's script suffered from macro-averaging and lowercasing bugs, and used the flawed "tokens per word" metric. Using "tokens per sentence" revealed that **XLM-RoBERTa** offers the best cross-lingual parity and cost-efficiency.
* **Part B:** The severe throughput crash at batch 32 was diagnosed as **KV-cache thrashing**. The physical memory limit supports a maximum of ~25 concurrent 4096-token sequences.
* **Part C:** To achieve casual tone alignment within a strict 3-week deadline and limited GPU budget, we selected a **LoRA SFT** strategy with a strict Day-5 kill criterion.
