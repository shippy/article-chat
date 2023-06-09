from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    cognito_sub_id: str = Field(..., unique=True)
    is_disabled: bool = Field(default=False)