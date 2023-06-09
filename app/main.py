from typing import Annotated, Mapping
from fastapi import FastAPI, File, HTTPException, UploadFile
from langchain.embeddings.openai import OpenAIEmbeddings
# from openai import Embedding as OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from .models.document import Document
import boto3
import os

app = FastAPI()
s3_client = boto3.client("s3")
s3_bucket = os.environ.get("S3_BUCKET", "document-vectorizer")

@app.post("/upload_and_process_file/")
async def upload_and_process_file(
    uploaded_file: UploadFile = File(...),
) -> Mapping[str, int]:
    try:
        contents = uploaded_file.file.read()
        uploaded_file.file.seek(0)
        s3_client.upload_fileobj(
            uploaded_file.file, s3_bucket, uploaded_file.filename
        )
        
        # TODO: Chunk and extract embeddings from the file
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(contents)
        embedder = OpenAIEmbeddings()
        
        for doc in docs:
            ...
        
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
