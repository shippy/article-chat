from http import HTTPStatus
from typing import List
from fastapi.testclient import TestClient

import pytest
import pytest_asyncio
from sqlmodel import SQLModel, Session, create_engine

from unittest.mock import AsyncMock, MagicMock, patch

from app.main import app, get_session, get_current_user

# from app.core.auth import get_current_user
# from app.core.database import get_session
from app.models.document import Document, Chat, ChatMessage
from app.models.user import User

from .conftest import mock_get_current_user, mock_get_another_user


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
    assert all("chats" in doc for doc in response.json())


# Now ensure that unauthenticated users get a 401
@pytest.mark.asyncio
async def test_list_documents_unauthenticated(client: TestClient):
    response = client.get("/documents")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


# Now ensure that users only get their own documents
@pytest.mark.asyncio
async def test_list_documents_unauthorized(
    client: TestClient, documents: List[Document]
):
    app.dependency_overrides[get_current_user] = mock_get_another_user
    response = client.get("/documents")
    app.dependency_overrides.clear()
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_list_messages_in_chat(
    client: TestClient,
    documents: List[Document],
    chats: List[Chat],
):
    app.dependency_overrides[get_current_user] = mock_get_current_user
    response = client.get(f"/documents/{documents[0].id}/chat/{chats[2].id}")
    app.dependency_overrides.clear()
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_messages_in_chat_unauthenticated(
    client: TestClient,
    documents: List[Document],
    chats: List[Chat],
):
    response = client.get(f"/documents/{documents[0].id}/chat/{chats[2].id}")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    
@pytest.mark.asyncio
async def test_list_messages_in_chat_unauthorized(
    client: TestClient,
    documents: List[Document],
    chats: List[Chat],
):
    app.dependency_overrides[get_current_user] = mock_get_another_user
    response = client.get(f"/documents/{documents[0].id}/chat/{chats[2].id}")
    app.dependency_overrides.clear()
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0
