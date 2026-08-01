# AI Usage Summary

I used Antigravity and Codex during this assignment. Will breakdown and record the steps and observations.

### Where it helped
#### Step 1:
- **Setting up environment & testing:** The AI set up the base environment, ran procedural testing, and recorded the results in `Observation.md`.
- **Spotting the math bugs:** The AI reviewed the intern's script, instantly caught the macro-averaging and lowercase bugs, and correctly explained why "tokens per sentence" is linguistically better than "tokens per word."

#### Step 2:
- **Setting up the download scripts:** The AI wrote the Python scripts to fetch the FLORES and IN22 datasets, automating the API calls and file saving.

### Where it misled me
- **The OPUS dataset hallucination:** The AI recommended OPUS-100 as a conversational dataset. I had to scrap it because it was bilingual (not strictly n-way parallel) and heavily polluted with religious and software text instead of casual subtitles.

