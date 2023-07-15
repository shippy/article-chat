from typing import Annotated, Mapping
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from fastapi_cognito import CognitoToken
import httpx
from langchain.embeddings.openai import OpenAIEmbeddings

# from openai import Embedding as OpenAIEmbeddings
import tempfile
import os

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from sqlmodel import SQLModel, Session, select
from typing import Union, Sequence

from .core.settings import settings
from .core.database import get_session, engine
from .core.auth import cognito_eu
from .models.document import Document, VectorEmbedding
from .models.user import User
from .models.chat import Chat, ChatMessage
import boto3
import os

app = FastAPI()
CHUNK_SIZE = 1000

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     return ...


async def extract_embeddings_from_file(
    uploaded_file: UploadFile, session: Session
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

    # current_user = select(User).where(User.cognito_id == token.cognito_id).first()
    current_user = session.exec(select(User).where(User.id == 1)).first()
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
    session=Depends(get_session),
) -> int:
    try:
        # contents = uploaded_file.file.read()
        # uploaded_file.file.seek(0)
        # await upload_file(uploaded_file)
        document_id = await extract_embeddings_from_file(uploaded_file, session)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {e}")
    finally:
        uploaded_file.file.close()
        
    return document_id
    # return RedirectResponse(url=f"/documents/{document_id}/new_chat")


@app.get("/documents/{document_id}/new_chat")
async def create_new_chat(document_id: int, session: Session = Depends(get_session)) -> int:
    new_chat = Chat(document_id=document_id)
    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)
    
    return new_chat.id
    
    
@app.get("/chats/{chat_id}")
async def retrieve_chat(chat_id: int, session: Session = Depends(get_session)) -> Sequence[ChatMessage]:
    # TODO: Limit to current user
    query = select(ChatMessage).where(ChatMessage.chat_id == chat_id)
    chat_messages = session.exec(query)
    return chat_messages


@app.post("/chats/{chat_id}/message")
async def send_message(chat_id: int, message: str):
    return


@app.get("/login")
async def login(auth: CognitoToken = Depends(cognito_eu.auth_required)) -> Mapping[str, str]:
    return {"message": "Login successful", "username": auth.username}


# @app.get("/callback")
# async def process_cognito_callback(code: str):
#     data = {
#         "grant_type": "authorization_code",
#         "client_id": settings.cognito_client_id,
#         "client_secret": settings.cognito_client_secret,
#         "code": code,
#         "redirect_uri": settings.cognito_redirect_uri,
#     }
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             settings.cognito_token_url, data=data, headers=headers
#         )
#     if response.status_code != 200:
#         raise HTTPException(status_code=401, detail="Invalid callback code")

@app.get("/callback")
async def process_cognito_callback(auth: CognitoToken = Depends(cognito_eu.auth_required)):
    return auth

@app.get("/redirect")
async def redirect_from_cognito(auth: CognitoToken = Depends(cognito_eu.auth_required)):
    return auth


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    try:
        base_user = User(username="simon.podhajsky@gmail.com")
        with Session(engine) as session:
            session.add(base_user)
            session.commit()
    except Exception as e:
        pass