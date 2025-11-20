from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    preference_vector: List[float] = Field(sa_column=Column(Vector(384))) # all-MiniLM-L6-v2 dimension
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Tweet(SQLModel, table=True):
    id: str = Field(primary_key=True) # Tweet ID from X
    text: str
    author_id: str
    created_at: datetime
    embedding: List[float] = Field(sa_column=Column(Vector(384)))
    metadata_json: str = Field(default="{}") # Store extra fields as JSON string

class Swipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    tweet_id: str = Field(foreign_key="tweet.id")
    action: str # "LIKE" or "DISCARD"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
