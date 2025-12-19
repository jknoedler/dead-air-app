# backend/models.py

from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserPlatformToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    platform: str = Field(nullable=False)
    access_token: str = Field(nullable=False)
    refresh_token: str = Field(nullable=True)
    expires_at: datetime = Field(nullable=True)

class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    platform: str = Field(nullable=False)
    platform_post_id: str = Field(nullable=False)
    posted_at: datetime = Field(default_factory=datetime.utcnow)

class DailyActivity(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: datetime = Field(nullable=False)
    opened: bool = Field(default=False)
    posted: bool = Field(default=False)
    eligible_for_refund: bool = Field(default=True)
