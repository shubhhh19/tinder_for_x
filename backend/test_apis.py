import os
import requests
import tweepy
from dotenv import load_dotenv

# Load environment variables from the parent directory .env or current directory
load_dotenv(dotenv_path="../.env")
load_dotenv()

def test_huggingface():
    print("\n--- Testing Hugging Face API ---")
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ HUGGINGFACE_API_KEY not found in .env")
        return False
    
    print(f"Found API Key: {api_key[:4]}...{api_key[-4:]}")
    
    API_URL = "https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": ["This is a test sentence to verify the API."],
        "options": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) == 384: # MiniLM-L6-v2 dim
                print("✅ Hugging Face API is working! (Embedding generated)")
                return True
            else:
                print(f"⚠️ API returned unexpected data format: {type(data)}")
                return False
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_twitter():
    print("\n--- Testing X (Twitter) API ---")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("❌ TWITTER_BEARER_TOKEN not found in .env")
        return False
        
    print(f"Found Bearer Token: {bearer_token[:4]}...{bearer_token[-4:]}")
    
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        # Search for one recent tweet to verify access
        response = client.search_recent_tweets(query="Python", max_results=10)
        
        if response.data:
            print(f"✅ X API is working! Fetched {len(response.data)} tweets.")
            return True
        elif response.meta and response.meta.get('result_count') == 0:
             print("✅ X API is working! (No tweets found for query, but auth is good)")
             return True
        else:
            print("⚠️ X API returned no data (Check permissions or query)")
            return False
            
    except tweepy.errors.Unauthorized:
        print("❌ Unauthorized: Check your Bearer Token.")
        return False
    except tweepy.errors.Forbidden:
        print("❌ Forbidden: Your access level might not support this endpoint (Basic tier required for search).")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Starting API Verification...")
    hf_status = test_huggingface()
    x_status = test_twitter()
    
    if hf_status and x_status:
        print("\n🎉 All External APIs are configured correctly!")
    else:
        print("\n⚠️ Some APIs failed. Please check your .env file.")
