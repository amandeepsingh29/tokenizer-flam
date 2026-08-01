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

*Note: The mathematically correct denominator is "Tokens per Sentence", because a parallel sentence holds the semantic payload of information constant across languages.*
