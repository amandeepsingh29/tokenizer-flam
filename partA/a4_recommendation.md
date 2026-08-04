# Recommendation Memo

## Corrected Headline Numbers

After evaluating our Multilingual Eval Corpus (spanning Encyclopedic, News, and Conversational domains) using the corrected semantic metric (**Tokens per Sentence**), we found that tokenizers drastically change the hardware compute requirements for our Indic users.

Below is the complete dataset breakdown of Tokens per Sentence and the cross-language fertility multiplier (relative to English) for our four tokenizers.

### 1. Legacy Baseline (GPT-2)
The old BPE tokenizer heavily penalizes Indic languages, effectively making them 7x to 15x more expensive.
| Dataset | English | Hindi | Tamil | Kannada |
| :--- | :--- | :--- | :--- | :--- |
| **FLORES-200** | 26.72 | 198.09 (7.41x) | 415.19 (15.54x) | 363.05 (13.59x) |
| **IN22-Gen** | 32.98 | 239.71 (7.27x) | 499.88 (15.16x) | 449.55 (13.63x) |
| **IN22-Conv** | 12.28 | 81.10 (6.60x) | 172.03 (14.01x) | 149.59 (12.18x) |

### 2. Modern Standard (GPT-4o)
The massive `o200k_base` vocabulary significantly compresses Indic text, dropping the multiplier to ~1.5x - 2.0x.
| Dataset | English | Hindi | Tamil | Kannada |
| :--- | :--- | :--- | :--- | :--- |
| **FLORES-200** | 26.55 | 41.77 (1.57x) | 52.57 (1.98x) | 52.28 (1.97x) |
| **IN22-Gen** | 32.77 | 50.68 (1.55x) | 66.90 (2.04x) | 69.36 (2.12x) |
| **IN22-Conv** | 12.01 | 17.11 (1.43x) | 22.74 (1.89x) | 25.29 (2.11x) |

### 3. Open Source Standard (Llama-3 128k)
While much better than GPT-2, Llama-3 still struggles with Dravidian languages compared to GPT-4o, costing ~7x - 8x more than English.
| Dataset | English | Hindi | Tamil | Kannada |
| :--- | :--- | :--- | :--- | :--- |
| **FLORES-200** | 26.85 | 67.70 (2.52x) | 205.31 (7.65x) | 237.82 (8.86x) |
| **IN22-Gen** | 33.30 | 81.58 (2.45x) | 246.87 (7.41x) | 295.00 (8.86x) |
| **IN22-Conv** | 12.27 | 27.85 (2.27x) | 85.59 (6.98x) | 97.81 (7.97x) |

### 4. Multilingual Specialist (XLM-Roberta)
The absolute best compression for Indic languages, dropping the penalty to near parity (~1.3x).
| Dataset | English | Hindi | Tamil | Kannada |
| :--- | :--- | :--- | :--- | :--- |
| **FLORES-200** | 30.30 | 37.77 (1.25x) | 40.87 (1.35x) | 40.99 (1.35x) |
| **IN22-Gen** | 37.12 | 45.07 (1.21x) | 51.80 (1.40x) | 55.06 (1.48x) |
| **IN22-Conv** | 13.33 | 15.59 (1.17x) | 16.32 (1.22x) | 19.55 (1.47x) |

## Denominator Comparison: Why "Tokens per Sentence"?

If we use the intern's original metric (**Tokens per Word**), Hindi appears **5.89x** more expensive than English. However, "Tokens per Word" is a fundamentally flawed metric because languages express the exact same semantic meaning using a different number of words (e.g., Hindi uses postpositions instead of prepositions, altering word counts). 

By changing the denominator to **Tokens per parallel sentence**, we hold the actual semantic payload of information constant. Under this mathematically rigorous denominator (on the GPT-2 baseline), the true multiplier for our dataset is actually **7.41x** for formal text. The choice of denominator drastically changes the apparent cost multiplier.

## Strategic Recommendations

**1. Routing Recommendation:**
Do not route all Indic traffic to a separate model yet. Instead, **upgrade our core tokenizer from GPT-2 to XLM-Roberta or GPT-4o (`o200k_base`)**. XLM-Roberta compresses Indic text so efficiently that the cost penalty drops to near parity (~1.2x - 1.4x), eliminating the need for a bifurcated, complex routing architecture and duplicated serving costs.

**2. The Biggest Caveat:**
Our Multilingual Eval Corpus consists of clean, grammatically correct sentences (Encyclopedic, News, structured Dialogue). **It cannot tell us how these tokenizers perform on highly informal, noisy user data.** If our real-world Indic users heavily code-mix (e.g., Hinglish/Tanglish), use internet slang, or typos, the real-world token efficiency could be vastly worse than our 1.3x baseline implies.

**3. Production Metric to Monitor:**
To catch this analysis being wrong in production, we must monitor the **`average_generated_tokens_per_request` segmented by `detected_language`**. If the ratio of Hindi generated tokens to English generated tokens spikes well beyond our predicted ~1.3x - 1.5x multiplier in production, it means real-world code-mixing or slang is defeating the tokenizer, and our capacity planning is compromised.
