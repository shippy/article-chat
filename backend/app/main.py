from typing import Mapping
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from app.core.settings import settings
from app.core.database import get_session, engine
from app.core.auth import (
    cognito_eu,
    get_current_user,
)
from app.api.auth_router import cognito_router
from app.api.document_router import document_router

app = FastAPI()
app.include_router(cognito_router, prefix="/auth")
app.include_router(document_router, prefix="/documents")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://journalarticle.chat",
        "https://www.journalarticle.chat",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Mapping[str, str]:
    return {"message": "App functioning"}


@app.on_event("startup")
def on_startup():
    from sqlalchemy.sql import text
    from app.models.document import (
        Chat,
        ChatMessage,
        ChatOriginator,
        Document,
        VectorEmbedding,
        DocumentWithChats,
    )
    from app.models.user import User

    with Session(engine) as session:
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        session.commit()
    SQLModel.metadata.create_all(engine)
