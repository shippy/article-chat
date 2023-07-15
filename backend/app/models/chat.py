from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Literal
from enum import Enum


class ChatOriginator(str, Enum):
    user = "user"
    ai = "ai"


class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(..., foreign_key="document.id")


class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    originator: ChatOriginator = Field(default=ChatOriginator.user)
    user_id: int
    chat_id: int = Field(..., foreign_key="chat.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)
