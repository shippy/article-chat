# Setup per https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/

import datetime
from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from typing import Generator, List
from app.main import app, get_session, get_current_user

from app.models.document import Document, Chat, ChatMessage
from app.models.user import User


def get_test_session() -> Session:  # Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        return session


@pytest.fixture(name="session")
def session_fixture() -> Session:
    return get_test_session()


async def mock_get_current_user():
    return User(id=1, username="testuser", cognito_id="aaaaaa-bbbbb-ccccc-ddddd")


async def mock_get_another_user():
    return User(id=2, username="testuser2", cognito_id="aaaaaa-bbbbb-ccccc-eeeee")


@pytest.fixture(name="client")
def client_fixture(session: Session) -> TestClient:
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user(session: Session) -> User:
    user = User(id=1, username="testuser", cognito_id="aaaaaa-bbbbb-ccccc-ddddd")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest_asyncio.fixture
async def documents(session: Session, user: User) -> List[Document]:
    documents = [
        Document(title="Document 1", user_id=user.id),
        Document(title="Document 2", user_id=user.id),
        Document(title="Document 3", user_id=user.id),
    ]
    session.add_all(documents)
    session.commit()
    for document in documents:
        session.refresh(document)
    return documents


@pytest_asyncio.fixture
async def semi_deleted_documents(session: Session, user: User) -> List[Document]:
    documents = [
        Document(title="Document 1", user_id=user.id),
        Document(title="Document 2", user_id=user.id, deleted_at=datetime.datetime.now()),
    ]
    
    session.add_all(documents)
    session.commit()
    for document in documents:
        session.refresh(document)
        
    return documents


@pytest_asyncio.fixture
async def chats(session: Session, documents: List[Document]) -> List[Chat]:
    chats = [
        Chat(document_id=documents[0].id, title="Chat 1"),
        Chat(document_id=documents[0].id, title="Chat 2"),
        Chat(document_id=documents[1].id, title="Chat 3"),
    ]
    session.add_all(chats)
    session.commit()
    for chat in chats:
        session.refresh(chat)

    messages = [
        ChatMessage(content="Message 1", chat_id=chats[0].id, user_id=1),
        ChatMessage(content="Message 2", chat_id=chats[1].id, user_id=2),
        ChatMessage(content="Message 3", chat_id=chats[2].id, user_id=1),
        ChatMessage(content="Message 4", chat_id=chats[2].id, user_id=1),
    ]
    session.add_all(messages)
    session.commit()

    return chats


@pytest_asyncio.fixture
async def semi_deleted_chats(session: Session, documents: List[Document]) -> List[Chat]:
    chats = [
        Chat(document_id=documents[0].id, title="Chat 1"),
        Chat(document_id=documents[0].id, title="Chat 2", deleted_at=datetime.datetime.now())
    ]
    
    session.add_all(chats)
    session.commit()
    for chat in chats:
        session.refresh(chat)
        
    return chats