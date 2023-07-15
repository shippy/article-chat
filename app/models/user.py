from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(..., unique=True)
    cognito_id: str = Field(None, unique=True)
    session_id: UUID = Field(None, unique=True)
    is_disabled: bool = Field(default=False)