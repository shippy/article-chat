from typing import Annotated, Mapping
from fastapi import Body, Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from fastapi_cognito import CognitoToken
import httpx
from langchain.embeddings.openai import OpenAIEmbeddings

# from openai import Embedding as OpenAIEmbeddings
import tempfile
import os

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, col, select
from typing import Annotated, Sequence, Union

from app.core.settings import settings
from app.core.database import get_session, engine
from app.core.auth import (
    cognito_eu,
    get_current_user,
)
from app.models.document import Chat, ChatMessage, ChatOriginator, Document, VectorEmbedding, DocumentWithChats
from app.models.user import User
from app.api.auth_router import cognito_router
import os

app = FastAPI()
app.include_router(cognito_router, prefix="/auth")
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
CHUNK_SIZE = 1000

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     return ...


async def extract_embeddings_from_file(
    uploaded_file: UploadFile,
    session: Session,
    current_user: User,
) -> int:
    try:
        # Get the contents of the uploaded file
        contents = await uploaded_file.read()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            # Write the contents of the uploaded file to the temporary file
            temp.write(contents)
            temp.flush()  # Ensure data is written
            loader = UnstructuredPDFLoader(temp.name)
            loaded_document = loader.load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file in: {e}")

    splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=100)
    docs = splitter.split_documents(loaded_document)

    db_doc = Document(title=uploaded_file.filename, user_id=current_user.id)
    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)

    embedder = OpenAIEmbeddings()
    chunks_to_embed = [text.page_content for text in docs]
    vectors = embedder.embed_documents(chunks_to_embed)
    db_vectors = [
        VectorEmbedding(document_id=db_doc.id, embedding=vector, content=content)
        for vector, content in zip(vectors, chunks_to_embed)
    ]
    for db_vector in db_vectors:
        session.add(db_vector)

    session.commit()

    return db_doc.id


@app.get("/")
async def root() -> Mapping[str, str]:
    return {"message": "App functioning"}


@app.post("/upload_and_process_file/")
async def upload_and_process_file(
    uploaded_file: UploadFile = File(...),
    # token: CognitoToken = Depends(cognito_eu.auth_required),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> int:
    try:
        # contents = uploaded_file.file.read()
        # uploaded_file.file.seek(0)
        # await upload_file(uploaded_file)
        document_id = await extract_embeddings_from_file(
            uploaded_file, session, current_user=current_user
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {e}")
    finally:
        uploaded_file.file.close()

    return document_id
    # return RedirectResponse(url=f"/documents/{document_id}/new_chat")


@app.get("/documents")
async def list_documents(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Sequence[DocumentWithChats]:
    query = select(Document).where(Document.user_id == current_user.id).order_by(col(Document.created_at).desc())
    documents = list(session.exec(query))
    return documents


@app.get("/documents/{document_id}/new_chat")
async def create_new_chat(
    document_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> int:
    # TODO: Check that the document belongs to the user
    new_chat = Chat(document_id=document_id)
    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)

    return new_chat.id


@app.get("/documents/{document_id}/chat/{chat_id}")
async def retrieve_chat(
    document_id: int,
    chat_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Sequence[ChatMessage]:
    query = select(ChatMessage).where(
        ChatMessage.chat_id == chat_id, ChatMessage.user_id == current_user.id
    )
    chat_messages = session.exec(query)
    return list(chat_messages)


def get_k_similar_chunks(
    query_embedding: Sequence[float], session: Session, k: int = 3
) -> Sequence[str]:
    query = (
        select(VectorEmbedding.content)
        .order_by(VectorEmbedding.embedding.l2_distance(query_embedding))
        .limit(k)
    )
    results = session.exec(query)

    return list(results)


TEMPLATE = """
You are a good chatbot that answers questions regarding published journal papers. You are academic and precise.

The relevant chunks of the paper are:

- {chunks}.

"""
# Please respond to the following question or request: {query}


def make_submittable_prompt(
    message: str, relevant_docs: Sequence[str], template: str = TEMPLATE
) -> str:
    bullet_points = "- " + "\n- ".join(relevant_docs)
    prompt = template.format(chunks=bullet_points)
    return prompt


@app.post("/documents/{document_id}/chat/{chat_id}/message")
async def send_message(
    document_id: int,
    chat_id: int,
    # FIXME: Should this be message: str = Body(..., embed=True)?
    message: Annotated[str, Body(embed=True)],
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ChatMessage:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

    new_message = ChatMessage(chat_id=chat_id, user_id=current_user.id, content=message)

    msg_embedding = OpenAIEmbeddings().embed_documents([message])[0]
    relevant_docs = get_k_similar_chunks(msg_embedding, session)

    gpt_prompt = make_submittable_prompt(message, relevant_docs)

    chat = ChatOpenAI(model="gpt-4", temperature=0)
    # TODO: Add some prior chat messages to the prompt?
    response = chat(
        [
            SystemMessage(content=gpt_prompt),
            HumanMessage(content=message),
        ]
    )
    ai_response = ChatMessage(
        chat_id=chat_id,
        user_id=current_user.id,
        content=response.content,
        originator=ChatOriginator.ai,
    )
    
    session.add_all([new_message, ai_response])
    session.commit()
    session.refresh(ai_response)
    
    return ai_response


@app.on_event("startup")
def on_startup():
    from sqlalchemy.sql import text

    with Session(engine) as session:
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        session.commit()
    SQLModel.metadata.create_all(engine)
