import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app
from app.services.chat_service import ChatService
from app.models.chat_models import ChatResponse
from app.api.chat_routes import get_chat_service

@pytest.fixture
def mock_chat_service():
    return AsyncMock(spec=ChatService)

@pytest.fixture
def client(mock_chat_service):
    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_successful_chat_interaction(client, mock_chat_service):
    # Arrange
    test_message = "Hello, AI!"
    mock_response = "This is a mock response"
    mock_chat_service.process_message.return_value = ChatResponse(response=mock_response)

    # Act
    response = client.post("/api/chat", json={"message": test_message})

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json()["response"], str)
    assert len(response.json()["response"]) > 0
    assert response.json() == {"response": mock_response}
    mock_chat_service.process_message.assert_awaited_once_with(test_message)

@pytest.mark.asyncio
async def test_chat_error_handling(client, mock_chat_service):
    # Arrange
    test_message = "Trigger an error"
    mock_chat_service.process_message.side_effect = Exception("Test error")

    # Act
    response = client.post("/api/chat", json={"message": test_message})

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Test error"}

@pytest.mark.asyncio
async def test_get_conversation_history(client, mock_chat_service):
    # Arrange
    expected_history = [["user", "Hello"], ["ai", "Hi there!"]]
    mock_chat_service.get_conversation_history.return_value = expected_history

    # Act
    response = client.get("/api/conversation")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"history": expected_history}
    assert isinstance(response.json()["history"], list)
    assert len(response.json()["history"]) == len(expected_history)

def test_clear_conversation(client, mock_chat_service):
    # Act
    response = client.post("/api/clear")

    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")

    # Assert
    assert response.status_code == 204
    mock_chat_service.clear_conversation.assert_called_once()


def test_clear_conversation_error_handling(client, mock_chat_service):
    # Arrange
    mock_chat_service.clear_conversation.side_effect = Exception("Test error")

    # Act
    response = client.post("/api/clear")


    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Test error"}