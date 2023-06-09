from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    user_id: int
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)