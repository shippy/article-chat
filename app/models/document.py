from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Sequence
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(..., max_length=100)
    user_id: int = Field(foreign_key="user.id")
    
    created_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)
    
class sVectorEmbedding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(..., foreign_key="document.id")
    embedding: Sequence[float] = Field(..., sa_column=Column(Vector(1536)))
    
    created_at: datetime = Field(default_factory=datetime.now)
