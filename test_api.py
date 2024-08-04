# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_chat_endpoint():
    url = f"{BASE_URL}/chat"
    payload = {"message": "What are the best materials for energy-efficient windows? Keep your response under 20 words."}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    print("Chat Endpoint Test:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_conversation_endpoint():
    url = f"{BASE_URL}/conversation"
    response = requests.get(url)
    print("Conversation Endpoint Test:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_clear_endpoint():
    url = f"{BASE_URL}/clear"
    response = requests.post(url)
    print("Clear Endpoint Test:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print()

if __name__ == "__main__":
    test_chat_endpoint()
    test_conversation_endpoint()
    test_clear_endpoint()
    # Test chat endpoint again to see if the conversation was cleared
    test_conversation_endpoint()
    test_chat_endpoint()
    test_conversation_endpoint()