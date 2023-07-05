from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    # username: str = Field(unique=True)
    cognito_id: str = Field(..., unique=True)
    is_disabled: bool = Field(default=False)