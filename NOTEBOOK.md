# Lab Notebook

**Step 1:** Record observations in `Observation.md`

**Step 2:** Get back to assignment Part A
## Part A1: Multilingual Eval Corpus

We have built a new parallel evaluation corpus combining three distinct datasets:
1. **FLORES-200** (`muennighoff/flores200`): 997 strictly n-way parallel sentences covering the formal/Wikipedia domain.
2. **IN22-Gen** (`ai4bharat/IN22-Gen`): 1024 strictly n-way parallel sentences created explicitly for evaluating Indic language models (General/News domain).
3. **IN22-Conv** (`ai4bharat/IN22-Conv`): Strictly n-way parallel sentences focusing heavily on conversational dialogue and spoken language.

- **Languages:** English (`eng_Latn`), Hindi (`hin_Deva`), Tamil (`tam_Taml`), Kannada (`kan_Knda`).
- **Domain:** Encyclopedic, News, and Conversational Dialogue.
- **Preprocessing:** Extracted directly to clean `.txt` files.

Note: **OPUS-100**: *REJECTED due to bilingual format.*
