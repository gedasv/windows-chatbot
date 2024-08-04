import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Window Manufacturing Chatbot API"}

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_flow(client):
    test_message = "What are the types of windows available?"
    response = client.post("/api/chat", json={"message": test_message})
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)
    assert len(response.json()["response"]) > 0

def test_multiple_chat_interactions(client):
    messages = [
        "What are the most energy-efficient windows?",
        "How much do they cost?",
        "Can you compare them with standard windows?"
    ]
    
    for message in messages:
        response = client.post("/api/chat", json={"message": message})
        assert response.status_code == 200
        assert "response" in response.json()
        assert isinstance(response.json()["response"], str)
        assert len(response.json()["response"]) > 0

def test_invalid_input(client):
    # Test empty message
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422
    assert "String should have at least 1 character" in response.json()["detail"][0]["msg"]

    # Test whitespace-only message
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 422
    assert "Message cannot be empty or just whitespace" in response.json()["detail"]

    # Test message that's too long
    # Assuming that it's 1000 characters
    long_message = "a" * 1001
    response = client.post("/api/chat", json={"message": long_message})
    assert response.status_code == 422
    assert "String should have at most 1000 characters" in response.json()["detail"][0]["msg"]

    # Test invalid JSON
    response = client.post("/api/chat", json={"invalid_key": "some message"})
    assert response.status_code == 422