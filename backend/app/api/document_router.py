from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
)
from fastapi.responses import JSONResponse, RedirectResponse
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter

from sqlmodel import Session, col, select
import tempfile
from typing import Annotated, Sequence, Union


from app.core.database import get_session, engine
from app.core.auth import get_current_user
from app.models.document import (
    Chat,
    ChatMessage,
    ChatOriginator,
    Document,
    VectorEmbedding,
    DocumentWithChats,
)
from app.models.user import User

document_router = APIRouter()

CHUNK_SIZE = 1000


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

    document_name = uploaded_file.filename or "Untitled"

    db_doc = Document(title=document_name, user_id=current_user.id)
    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)

    embedder = OpenAIEmbeddings()  # type: ignore
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


@document_router.post("/upload")
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


@document_router.get("/", response_model=Sequence[DocumentWithChats])
async def list_documents(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Sequence[Document]:
    query = (
        select(Document).where(Document.user_id == current_user.id)
        .order_by(col(Document.created_at).desc())
    )
    documents = list(session.exec(query))
    return documents


@document_router.get("/{document_id}/new_chat")
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

    return new_chat.id  # type: ignore


@document_router.get("/{document_id}/chat/{chat_id}")
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
    query_embedding: Sequence[float], document_id: int, session: Session, k: int = 3
) -> Sequence[str]:
    query = (
        select(VectorEmbedding.content)
        .where(VectorEmbedding.document_id == document_id)
        .order_by(VectorEmbedding.embedding.l2_distance(query_embedding))  # type: ignore
        .limit(k)
    )
    results = session.exec(query)

    return list(results)


TEMPLATE = """
You are a good chatbot that answers questions regarding published journal papers. 
You are academic and precise, but can expand your response to up to three paragraphs
if the response requires it.

The chunks of the paper relevant to the following question are:

- {chunks}.

"""
# Please respond to the following question or request: {query}


def make_submittable_prompt(
    message: str, relevant_docs: Sequence[str], template: str = TEMPLATE
) -> str:
    bullet_points = "- " + "\n- ".join(relevant_docs)
    prompt = template.format(chunks=bullet_points)
    return prompt


@document_router.post("/{document_id}/chat/{chat_id}/message")
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

    msg_embedding = OpenAIEmbeddings().embed_documents([message])[0]  # type: ignore
    relevant_docs = get_k_similar_chunks(
        query_embedding=msg_embedding, document_id=document_id, session=session
    )

    gpt_prompt = make_submittable_prompt(message, relevant_docs)

    chat = ChatOpenAI(model="gpt-4", temperature=0)  # type: ignore
    previous_messages_query = (
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .order_by(col(ChatMessage.created_at).desc())
        .limit(2)
    )
    previous_messages = session.exec(previous_messages_query)
    previous_messages_scaled = [
        AIMessage(content=x.content)
        if x.originator == "ai"
        else HumanMessage(content=x.content)
        for x in previous_messages
    ]
    # Only add the system message if there are previous messages
    if len(previous_messages_scaled) > 0:
        previous_messages_scaled = [
            SystemMessage(
                content="The previous two messages from this conversation are. Please take "
                f"them into consideration only if they are relevant to the question: {message}"
            )
        ] + previous_messages_scaled
    response = chat(
        [
            *previous_messages_scaled,
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
