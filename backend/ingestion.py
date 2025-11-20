import tweepy
import os
from typing import List
from .models import Tweet
from .core import get_embedding
from sqlmodel import Session
from datetime import datetime

# X API Client
def get_twitter_client():
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        return None
    return tweepy.Client(bearer_token=bearer_token)

def fetch_and_ingest_tweets(session: Session, query: str = "AI OR Machine Learning -is:retweet lang:en", max_results: int = 10):
    client = get_twitter_client()
    if not client:
        print("Twitter client not initialized")
        return

    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "author_id", "public_metrics", "lang"],
            expansions=["author_id"]
        )
        
        if not response.data:
            print("No tweets found")
            return

        tweets = response.data
        
        for t in tweets:
            # Check if tweet already exists
            if session.get(Tweet, t.id):
                continue
                
            # Generate embedding
            embedding = get_embedding(t.text)
            
            # Create Tweet object
            tweet_obj = Tweet(
                id=str(t.id),
                text=t.text,
                author_id=str(t.author_id),
                created_at=t.created_at or datetime.utcnow(),
                embedding=embedding,
                metadata_json=str(t.public_metrics)
            )
            
            session.add(tweet_obj)
        
        session.commit()
        print(f"Ingested {len(tweets)} tweets")
        
    except Exception as e:
        print(f"Error ingesting tweets: {e}")
