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
async def test_get_conversation_history(client: TestClient, mock_chat_service):
    # Arrange
    expected_history = [["user", "Hello"], ["ai", "Hi there!"]]
    expected_context_info = {"current_length": 2, "max_length": 10}
    
    mock_chat_service.get_conversation_history = AsyncMock(return_value=expected_history)
    mock_chat_service.get_context_info.return_value = expected_context_info

    # Act & Assert for default behavior (without context)
    response = client.get("/api/conversation")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["history"] == expected_history
    # assert "context_info" not in response_json

    # Act & Assert with context included
    response = client.get("/api/conversation?include_context=true")
    assert response.status_code == 200
    assert response.json() == {
        "history": expected_history,
        "context_info": expected_context_info
    }

    # Verify method calls
    assert mock_chat_service.get_conversation_history.call_count == 2
    assert mock_chat_service.get_context_info.call_count == 1

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