# DECISION MEMO
**Tone Casualization Across Six Indic Languages**

**Objective:** Inject a casual, conversational tone in Hindi, Kannada, Tamil, Telugu, Bengali, and Marathi for V1 in three weeks.
**Constraints:** 1× A100-80GB for two weeks; one Hindi/Kannada QA reviewer for 30 hours; $0 API budget.

**RECOMMENDATION:** Choose Path A: LoRA SFT on locally generated casualized pairs, with a Hindi/Kannada validation gate before scaling.

## Assumptions
* The base model already has acceptable semantic competence in all six languages; the gap is primarily tone.
* An open-weight local teacher can produce useful synthetic casualization pairs without paid APIs.
* LoRA training and evaluation can finish within the available A100 window and can be merged for serving.

## Back-of-envelope arithmetic
* **Compute:** 14 days × 24 hours = 336 A100-hours available for local generation, LoRA training, and evaluation.
* **Reviewer throughput:** 60 pairs/hour × 30 hours = 1,800 reviewed pairs; allocate 900 Hindi + 900 Kannada.
* **Data volume:** 1,000 pairs/language × 6 = ~6,000 pairs; 4,200 pairs in the other four languages receive automated checks plus sampling, not native review.
* **Cost:** $0 API spend. LoRA uses existing compute; merged adapters add no extra model call, with a target of <5% latency increase.

## Path analysis
* **A — LoRA SFT (choose):** Most consistent style control without another inference-time model. Main risk: synthetic phrasing may be unnatural in four languages without native review.
* **B — ≤1B rewriter (reject):** Adds TTFT, serving complexity, and a second multilingual failure point; a small model is especially exposed to morphology, dialect and unwanted English fallback.
* **C — Prompt only (fallback):** Fast and free, but tone instructions can lose priority across tasks, safety rules, formatting demands, and long conversations.

## Success metrics
| Metric | Launch threshold |
| :--- | :--- |
| **Hindi/Kannada blind A/B preference** | ≥70% prefer SFT output |
| **Meaning preservation** | ≥95% unchanged meaning |
| **Task-quality regression** | ≤2% absolute drop |
| **Severe language-quality errors** | <5% in sampled outputs |
| **Serving latency** | <5% increase; no extra model call |

## Kill criteria — decide by end of Day 5
* Abandon SFT and ship the best prompt-only baseline if preference gain is <5 percentage points over prompt-only, task accuracy drops >2–3%, or the four non-reviewed languages show material degradation or inconsistent language behavior.

## Day-1 experiment
1. Create 1,000 local synthetic pairs (~170 per language) and train a small LoRA.
2. Compare current, prompt-only, and LoRA-SFT outputs; manually review 200 Hindi/Kannada samples and run meaning, language-ID/code-mixing, task-quality, and latency checks across all six languages.
3. Scale toward 6,000 pairs only if SFT clears the quality gates and clearly beats prompt-only; otherwise keep prompt-only as the launch fallback.
