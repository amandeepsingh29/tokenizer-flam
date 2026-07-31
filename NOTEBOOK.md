# Lab Notebook

## Part A2: Tokenizer Audit (`fertility.py`)

I reviewed the intern's `fertility.py` script and found the following flaws:

### 1. Code Bug: Lowercasing before tokenization
- **Isolation:** On line 60, the script does `line = line.lower()` before passing the text to the tokenizer.
- **Effect:** The GPT-2 tokenizer is case-sensitive and was trained on cased text. Lowercasing English text forces the tokenizer into sub-optimal, less frequent tokenizations for words that are normally capitalized. It rarely affects Hindi, meaning it disproportionately penalizes English.
- **Magnitude:** When removed, English fertility drops from 1.265 to 1.229 (a distortion of +0.036 tokens/word). Hindi stays at 7.448. The bug artificially makes English look worse, shrinking the apparent gap (ratio changes from 6.06x down to the reported 5.89x).

### 2. Code Bug: Macro-averaging instead of Micro-averaging
- **Isolation:** On line 67, the script computes `sum(per_line_fertility) / n`.
- **Effect:** Averaging the ratio per line gives short 2-word sentences the exact same mathematical weight as 50-word sentences. The mathematically correct way is a micro-average: `total_tokens / total_words`.
- **Magnitude:** When fixed, English fertility changes from 1.265 to 1.253, and Hindi from 7.448 to 7.403. The distortion is small but mathematically unsound.

### 3. Conceptual Problem: Using "Words" as the Denominator
- **Isolation:** The metric `len(tokens) / len(words)` (where words is just `line.split(" ")`).
- **Effect:** The denominator must hold the semantic payload constant across languages to be a fair comparison of cost. Hindi and English express the exact same meaning using different numbers of words due to grammar (e.g., Hindi postpositions vs. English prepositions). Furthermore, `.split(" ")` is an awful heuristic for word counting. 
- **Magnitude:** If we use a metric that actually holds semantic meaning constant—such as **Tokens per Sentence** (since this is a parallel corpus)—the penalty for Hindi drops significantly. English takes 9.900 tokens/sentence, and Hindi takes 45.900 tokens/sentence. The ratio drops from the intern's reported **5.89x to 4.64x**.

### 4. Suspicious but Harmless: NFC Normalization
- **Isolation:** On line 49, the script does `unicodedata.normalize("NFC", line)`.
- **Effect:** While it looks like it might be tampering with the text, normalizing to NFC (precomposed characters) is standard best practice for Unicode, especially for complex scripts like Devanagari (Hindi) which heavily use combining marks. It ensures consistent encoding and does not erroneously distort the token count.

---
*(Next step: I need to complete A1 and A3 by building a real multilingual corpus and running a corrected analysis using multiple tokenizers and denominators).*
