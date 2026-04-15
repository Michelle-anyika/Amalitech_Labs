from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass
def User:
    username: str
    email: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    id: Optional[int] = None
    follower_count: int = 0
    following_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
def Post:
    user_id: int
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
def Comment:
    post_id: int
    user_id: int
    content: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
def FeedItem:
    post_id: int
    author_id: int
    author_username: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    rank: int
