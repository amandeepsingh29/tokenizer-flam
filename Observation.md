The starter kit's `fertility.py` file has modeling flaws, but the provided results are genuine, no alterations in that.

Results are not fabricated but wrong due to modeling:
```text
tokenizer: gpt2
lang      fertility (tok/word)    tok/char
------------------------------------------
eng                       1.27       0.226
hin                       7.45       1.579
hin is 5.89x the fertility of eng (worse tokenization)
```

### Old modelling steps:
1. **File Reading:** Read the corpus text files line-by-line.
2. **Normalization:** Normalize the text using NFC Unicode normalization.
3. **Lowercasing:** Convert every line to lowercase (`line.lower()`).
4. **Tokenization:** Tokenize the line using the `gpt2` tokenizer.
5. **Word Counting:** Count the number of words by simply splitting the string by spaces (`len(line.split(" "))`).
6. **Per-line Ratio:** Calculate the fertility ratio *per line* (`len(tokens) / len(words)`).
7. **Macro-averaging:** Calculate the final score by taking the average of all the per-line ratios.

### Flaws in old modelling steps:
1. **Lowercasing English Text (Code Bug):** 
   - **Flaw:** Lowercasing case-sensitive English text forces the GPT-2 tokenizer (which is trained on cased text) into sub-optimal tokenization, artificially inflating the English token count.
   - **Distortion:** It shrinks the apparent gap between Hindi and English slightly, as it negatively impacts English but barely affects Hindi.

2. **Macro-average instead of Micro-average (Code Bug):** 
   - **Flaw:** The script averages the `tokens/words` ratio for each line individually. This mathematically weights a tiny 2-word sentence equally with a massive 50-word paragraph. 
   - **Correction:** It should use a micro-average (sum of all tokens across all lines / sum of all words across all lines).

3. **Using "Words" as the Denominator (Conceptual Flaw):** 
   - **Flaw:** "Tokens per word" is a fundamentally flawed metric for cross-language comparison. Hindi and English express the exact same semantic meaning using a different number of words (due to grammar rules like postpositions vs. prepositions). Furthermore, `.split(" ")` is an unreliable heuristic for counting words across different languages. 
   - **Correction:** The denominator must hold semantic meaning constant across languages. A fair comparison would be **Tokens per parallel sentence**. When corrected to Tokens per Sentence, the ratio drops significantly from 5.89x down to 4.64x.

4. **NFC Normalization (Suspicious but Harmless):** 
   - **Flaw:** While explicitly normalizing to NFC looks suspicious, it is actually standard best practice for handling Unicode (especially for scripts with combining marks like Devanagari) to ensure characters are consistently represented. This does *not* distort the numbers.