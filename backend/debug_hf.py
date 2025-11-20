import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}

def try_url(name, url, payload):
    print(f"\nTesting {name}: {url}")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            data = response.json()
            if isinstance(data, list):
                print(f"Shape: {len(data)}")
                if len(data) > 0:
                    print(f"Item type: {type(data[0])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

# 1. Pipeline URL on Router
try_url("Pipeline URL", 
        "https://router.huggingface.co/hf-inference/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
        {"inputs": "Test sentence", "options": {"wait_for_model": True}})

# 2. BGE Small
try_url("BGE Small", 
        "https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5",
        {"inputs": "Test sentence", "options": {"wait_for_model": True}})

# 3. Paraphrase MiniLM
try_url("Paraphrase MiniLM", 
        "https://router.huggingface.co/hf-inference/models/sentence-transformers/paraphrase-MiniLM-L6-v2",
        {"inputs": "Test sentence", "options": {"wait_for_model": True}})
