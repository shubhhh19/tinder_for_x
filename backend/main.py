from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from .models import User, Tweet, Swipe
from .core import update_user_vector, get_ranked_feed
import os
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/tinder_for_x")
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Tinder for X")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Tinder for X API is running"}

from .ingestion import fetch_and_ingest_tweets

@app.post("/ingest")
def ingest_tweets(session: Session = Depends(get_session)):
    fetch_and_ingest_tweets(session)
    return {"status": "Ingestion started"}

@app.get("/feed/{user_id}")
def get_feed(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        # Auto-create user for MVP
        user = User(id=user_id, username=f"user{user_id}", preference_vector=[0.0]*384)
        session.add(user)
        session.commit()
        session.refresh(user)
    
    # Get ranked tweets
    tweets = get_ranked_feed(user, session)
    return {"feed": tweets}

@app.post("/swipe")
def record_swipe(swipe: Swipe, session: Session = Depends(get_session)):
    session.add(swipe)
    
    user = session.get(User, swipe.user_id)
    tweet = session.get(Tweet, swipe.tweet_id)
    
    if user and tweet:
        update_user_vector(user, tweet, swipe.action)
        session.add(user)
    
    session.commit()
    return {"status": "recorded"}
