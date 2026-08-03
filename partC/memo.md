# Part C: Decision Memo (Tone Casualization)

**Objective:** Inject a casual/conversational tone across 6 Indic languages (Hindi, Kannada, Tamil, Telugu, Bengali, Marathi) for the V1 launch in 3 weeks.
**Constraints:** 1x A100-80GB (2 weeks), 1 QA reviewer (Hindi/Kannada only, 30 hours total), $0 API budget.

---

## 1. Constraint Analysis & Assumptions
* **Compute Headroom:** 336 hours of A100-80GB compute provides massive headroom for local synthetic data generation or LoRA training.
* **QA Bandwidth:** At ~1 minute to review/edit a single pair, our reviewer can process 60 pairs per hour. Over 30 hours, our absolute **QA throughput limit is 1,800 pairs** (strictly Hindi/Kannada). 
* **API Budget:** $0 means all synthetic data must be generated locally using open-weights models.

## 2. Path Analysis & Academic Justification

### Path C: Prompt Engineering Only
* **Cost:** $0 serving latency, zero training overhead.
* **Analysis (Reject):** **Fatal Capability Limit.** A 4B parameter model lacks the internal reasoning capacity to separate factual instruction following from complex, culture-specific stylistic constraints in non-English languages. 
* **Citation:** As formalized by *Kumar et al. (2026)* in *"Diagnosing and Repairing Persona Collapse in LLM Advice"* and supported by *"The Chameleon's Limit,"* small language models suffer from **"Persona Collapse."** When forced to maintain a complex persona via prompt engineering, they rapidly abandon the behavioral constraints and default to a homogeneous, generic tone, or actively hallucinate.

### Path B: Small Inference-Time Rewriter (≤1B)
* **Cost:** Severe UX Latency (serial TTFT generation).
* **Analysis (Reject):** **Linguistic Fragmentation.** If our 4B model struggles with morphologically rich Indic languages, a ≤1B model will be profoundly worse. 
* **Citation:** Research surrounding Indic LLMs (e.g., the *BharatGen / PARAM-1* framework) heavily documents **"Linguistic Fragmentation."** Models with extremely small parameter counts completely fail to handle the morphological richness and dialect variations of Indic languages, causing them to spew gibberish or revert to English. Training a ≤1B model to avoid this would require massive, highly curated datasets far exceeding our 1,800-pair QA budget. 

### Path A: SFT on Synthetic Data (The Winner)
* **Cost:** $0 serving latency (Parameter-Efficient Fine-Tuning (LoRA) adapters merge natively into base weights).
* **Data Volume:** We require ~6,000 synthetic pairs (1,000 per language). We will leverage the A100 to generate this data locally. 
* **The QA Strategy ("Synthetic Extrapolation"):** We use our 1,800-pair QA budget to exhaustively verify 900 Hindi and 900 Kannada pairs. If the local teacher model produces high-quality data for those two, we extrapolate and blindly trust its zero-shot generation for the remaining 4,200 pairs in Tamil, Telugu, Bengali, and Marathi.
* **Analysis:** SFT is the industry standard to solve "Persona Collapse," baking the tone directly into the weights. This is the only mathematically viable path to hit all 6 languages under our constraints, provided we accept the QA extrapolation risk.

## 3. Recommendation & Metrics

I formally recommend proceeding with **Path (A) SFT on synthetic data** using the Synthetic Extrapolation strategy.

* **Success Metric:** Blind A/B Human Preference Win-Rate (SFT Model vs. Base Model).
* **Threshold:** The new SFT model must achieve a **>75% win-rate** on conversational prompts, while simultaneously displaying a **<5% regression** on our standard instruction-following benchmarks.

* **Kill Criterion:** If the local open-weights data generator produces synthetic Hindi/Kannada that fails the QA check (i.e., the reviewer rejects or edits >20% of the generated pairs due to Persona Collapse or Linguistic Fragmentation). 
* **By When:** End of **Week 1**. If the teacher model fails on the languages we *can* verify, it is definitively failing on the ones we *cannot* verify. If this threshold is breached, we must instantly abort the SFT path and pivot entirely to Prompt Engineering (Path C).

* **First Experiment (Day 1):** Run a 50-prompt Prompt Engineering (Path C) stress test on the base model and hand the raw outputs to the reviewer. This instantly tests the severity of the model's Persona Collapse. When it inevitably fails, the reviewer's manual corrections on those 50 prompts become the high-quality seed data for our A100 synthetic data generator.
