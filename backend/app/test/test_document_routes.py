from http import HTTPStatus
from typing import List, Generator

from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from pytest import fixture
import pytest_asyncio

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from unittest.mock import AsyncMock, MagicMock, patch

from app.main import app, get_session, get_current_user

# from app.core.auth import get_current_user
# from app.core.database import get_session
from app.models.document import Document
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


@fixture(name="session")
def session_fixture() -> Session:
    return get_test_session()


@fixture(name="client")
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


async def mock_get_current_user():
    return User(id=1, username="testuser", cognito_id="aaaaaa-bbbbb-ccccc-ddddd")


async def mock_get_another_user():
    return User(id=2, username="testuser2", cognito_id="aaaaaa-bbbbb-ccccc-eeeee")


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


@pytest.mark.asyncio
async def test_list_documents(
    client: TestClient,
    documents: List[Document],
):
    app.dependency_overrides[get_current_user] = mock_get_current_user
    response = client.get("/documents")
    app.dependency_overrides.clear()
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == len(documents)
    assert all(doc["title"] in [d.title for d in documents] for doc in response.json())


# Now ensure that unauthenticated users get a 401
@pytest.mark.asyncio
async def test_list_documents_unauthenticated(client: TestClient):
    response = client.get("/documents")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    
# Now ensure that users only get their own documents
@pytest.mark.asyncio
async def test_list_documents_unauthorized(client: TestClient, documents: List[Document]):
    app.dependency_overrides[get_current_user] = mock_get_another_user
    response = client.get("/documents")
    app.dependency_overrides.clear()
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0

