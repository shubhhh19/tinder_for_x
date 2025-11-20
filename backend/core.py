from typing import List
from .models import User, Tweet
import requests
import os
import time

# Hugging Face Inference API
HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def get_embedding(text: str) -> List[float]:
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("Warning: HUGGINGFACE_API_KEY not set. Returning zero vector.")
        return [0.0] * 384

    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": text,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching embedding from HF: {e}")
        return [0.0] * 384

def update_user_vector(user: User, tweet: Tweet, action: str):
    # Simple moving average
    alpha = 0.1
    tweet_vector = tweet.embedding
    user_vector = user.preference_vector
    
    if not user_vector:
        user.preference_vector = tweet_vector
        return

    new_vector = []
    for u, t in zip(user_vector, tweet_vector):
        if action == "LIKE":
            new_val = u + alpha * (t - u)
        else:
            new_val = u - (alpha * 0.5) * (t - u)
        new_vector.append(new_val)
    
    user.preference_vector = new_vector

def get_ranked_feed(user: User, db_session):
    # Placeholder
    return []
