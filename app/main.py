from typing import Annotated, Mapping
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi_cognito import CognitoToken
from langchain.embeddings.openai import OpenAIEmbeddings
# from openai import Embedding as OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from sqlmodel import Session, select
from typing import Union
from .core.database import get_session
from .core.auth import cognito_eu
from .models.document import Document, VectorEmbedding
from .models.user import User
import boto3
import os

app = FastAPI()
s3_client = boto3.client("s3")
s3_bucket = os.environ.get("S3_BUCKET", "document-vectorizer")

CHUNK_SIZE = 1000

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     return ...

async def upload_file(uploaded_file: UploadFile) -> bool:
    return s3_client.upload_fileobj(
        uploaded_file.file, s3_bucket, uploaded_file.filename
    )


async def get_embeddings_from_file(uploaded_file: UploadFile, contents: Union[str, bytes], session: Session) -> Document:
    splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=100)
    docs = splitter.split_documents(contents)
    embedder = OpenAIEmbeddings()
    
    current_user = select(User).where(User.cognito_id == token.cognito_id).first()
    db_doc = Document(title=uploaded_file.filename, user_id=current_user.id)
    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)
    
    vectors = embedder.embed_documents(docs, chunk_size=CHUNK_SIZE)
    db_vectors = [
        VectorEmbedding(document_id=db_doc.id, embedding=vector)
        for vector in vectors
    ]
    for db_vector in db_vectors:
        session.add(db_vector)
        
    session.commit()


@app.post("/upload_and_process_file/")
async def upload_and_process_file(
    uploaded_file: UploadFile = File(...),
    token: CognitoToken = Depends(cognito_eu.auth_required),
    session = Depends(get_session),
) -> Mapping[str, int]:
    try:
        contents = uploaded_file.file.read()
        uploaded_file.file.seek(0)
        # s3_client.upload_fileobj(
        #     uploaded_file.file, s3_bucket, uploaded_file.filename
        # )
        await upload_file(uploaded_file)
        
        # TODO: Chunk and extract embeddings from the file
        await get_embeddings_from_file(uploaded_file, contents)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {e}")
    finally:
        uploaded_file.file.close()
        
    return {"filename": 1}


@app.get("/chats/{chat_id}")
async def retrieve_chat(chat_id: int):
    return


@app.post("/chats/{chat_id}/message")
async def send_message(chat_id: int, message: str):
    return


@app.post('/signup')
async def signup():
    return  