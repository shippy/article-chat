from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import List, Optional, Sequence
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum


class DocumentBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(..., max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)


class Document(DocumentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    chats: List["Chat"] = Relationship(back_populates="document")


class DocumentWithChats(DocumentBase):
    id: int
    chats: List["Chat"] = []


class VectorEmbedding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(..., foreign_key="document.id")
    embedding: Sequence[float] = Field(..., sa_column=Column(Vector(1536)))
    content: str = Field(...)

    created_at: datetime = Field(default_factory=datetime.now)


class ChatOriginator(str, Enum):
    user = "user"
    ai = "ai"


class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(..., foreign_key="document.id")
    document: Document = Relationship(back_populates="chats")


class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    originator: ChatOriginator = Field(default=ChatOriginator.user)
    user_id: int
    chat_id: int = Field(..., foreign_key="chat.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)


DocumentWithChats.update_forward_refs()
