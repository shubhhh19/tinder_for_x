from typing import List
from .models import User, Tweet
import requests
import os
import time

# Hugging Face Inference API
HF_API_URL = "https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5"

def get_embedding(text: str) -> List[float]:
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("Warning: HUGGINGFACE_API_KEY not set. Returning zero vector.")
        return [0.0] * 384

    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": [text],
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

from sqlmodel import select
import random

def get_ranked_feed(user: User, db_session):
    # For now, just return random tweets that the user hasn't swiped on yet
    # In the future, this will use vector similarity
    
    # Get IDs of tweets user has already swiped
    # Note: This is inefficient for large datasets, but fine for MVP
    # swiped_query = select(Swipe.tweet_id).where(Swipe.user_id == user.id)
    # swiped_ids = db_session.exec(swiped_query).all()
    
    # Get random tweets
    # statement = select(Tweet).where(col(Tweet.id).notin_(swiped_ids)).limit(10)
    statement = select(Tweet).limit(20)
    results = db_session.exec(statement).all()
    
    # Shuffle them
    results = list(results)
    random.shuffle(results)
    
    return results[:10]
