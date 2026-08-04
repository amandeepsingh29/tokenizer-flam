# Part A1: Multilingual Eval Corpus

## 1. Corpus Composition
To properly evaluate token fertility across languages, we assembled a strict n-way parallel corpus across **4 languages**: English, Hindi, Tamil, and Kannada.

The final evaluation corpus contains **3,539 parallel sentences** per language, spanning three distinct datasets to ensure domain diversity:
* **FLORES-200** (1,012 sentences): Sourced from Wikipedia. Represents formal, encyclopedic syntax.
* **IN22-Gen** (1,024 sentences): Sourced from news, web articles, and general text. Represents standard written language.
* **IN22-Conv** (1,503 sentences): Sourced from dialogue and conversational data. Represents structured conversational text.

## 2. Preprocessing
The datasets were fetched directly from HuggingFace (`muennighoff/flores200` and `ai4bharat/IN22-*`). The only preprocessing applied was stripping leading/trailing whitespace (`strip()`). We explicitly chose **not** to enforce lowercasing or unicode normalization during the fetch step, as preserving the raw, native UTF-8 casing and text structure is essential for an honest tokenizer evaluation. 

## 3. What This Corpus Cannot Tell Us (Caveats)
While this corpus provides an excellent baseline for formal and standard conversational text, **it cannot tell us how the tokenizer performs on highly informal, noisy user data.** Real-world chat interactions are dominated by extreme internet slang, typos, emojis, and heavy code-mixing (e.g., Hinglish or Tanglish). Because our eval corpus consists of clean, grammatically correct sentences, our fertility multiplier calculations represent a "best-case scenario" for Indic languages. If users heavily code-mix in production, token efficiency could be vastly different than what this clean dataset implies.
