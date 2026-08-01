import os
# pyrefly: ignore [missing-import]
from datasets import load_dataset

def download_flores(out_dir):
    print("--- Downloading FLORES-200 ---")
    os.makedirs(out_dir, exist_ok=True)
    
    langs = {
        "eng": "eng_Latn",
        "hin": "hin_Deva",
        "tam": "tam_Taml",
        "kan": "kan_Knda"
    }
    
    for lang_code, hf_code in langs.items():
        print(f"Fetching {lang_code} from FLORES...")
        try:
            ds = load_dataset("muennighoff/flores200", hf_code, trust_remote_code=True)
            sentences = ds['dev']['sentence']
            
            out_path = os.path.join(out_dir, f"{lang_code}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                for s in sentences:
                    f.write(s.strip() + "\n")
            print(f"Saved {len(sentences)} lines to {out_path}")
        except Exception as e:
            print(f"Error loading {lang_code}: {e}")

def main():
    out_dir = "corpus"
    download_flores(out_dir)
    print("\nCorpus download complete!")

if __name__ == "__main__":
    main()
