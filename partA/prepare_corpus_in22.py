import os
# pyrefly: ignore [missing-import]
from datasets import load_dataset
# pyrefly: ignore [missing-import]
from huggingface_hub import login

def download_in22(out_dir, hf_token=None):
    if hf_token:
        print("Logging into Hugging Face...")
        login(token=hf_token)
        
    print("--- Downloading IN22-Gen ---")
    in22_dir = os.path.join(out_dir, "in22")
    os.makedirs(in22_dir, exist_ok=True)
    
    try:
        datasets_to_fetch = {
            "in22_gen": "ai4bharat/IN22-Gen",
            "in22_conv": "ai4bharat/IN22-Conv"
        }
        
        langs_map = {
            "eng": "eng_Latn",
            "hin": "hin_Deva",
            "tam": "tam_Taml",
            "kan": "kan_Knda"
        }
        
        for folder_name, repo_name in datasets_to_fetch.items():
            curr_dir = os.path.join(out_dir, folder_name)
            os.makedirs(curr_dir, exist_ok=True)
            
            print(f"Fetching {repo_name} n-way parallel dataset...")
            ds = load_dataset(repo_name, "default", split="test")
            
            for short_name, column_name in langs_map.items():
                out_path = os.path.join(curr_dir, f"{short_name}.txt")
                with open(out_path, "w", encoding="utf-8") as f:
                    for item in ds:
                        f.write(str(item[column_name]).strip() + "\n")
                        
            print(f"Successfully saved {len(ds)} n-way parallel sentences to {curr_dir}!")
            
    except Exception as e:
        print(f"\nError downloading IN22: {e}")
        print("\n========================================================")
        print("CRITICAL: IN22 is a gated dataset on Hugging Face.")
        print("You must do two things to download it:")
        print("1. Visit https://huggingface.co/datasets/ai4bharat/IN22-Gen AND https://huggingface.co/datasets/ai4bharat/IN22-Conv")
        print("   and click 'Agree and access repository' on BOTH pages.")
        print("2. Set your HF_TOKEN environment variable, or paste your token into this script.")
        print("========================================================\n")

from dotenv import load_dotenv

if __name__ == "__main__":
    out_dir = "corpus"
    
    # Load environment variables from .env
    load_dotenv()
    
    # Pass your HF token here to download the gated dataset
    HF_TOKEN = os.environ.get("HF_TOKEN", None)
    
    download_in22(out_dir, HF_TOKEN)
