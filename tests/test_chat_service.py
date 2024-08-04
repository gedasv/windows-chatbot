import pytest
import re
from unittest.mock import AsyncMock, MagicMock
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.utils.context_manager import ContextManager
from app.models.chat_models import ChatResponse


@pytest.fixture
def mock_llm_service():
    return AsyncMock(spec=LLMService)

@pytest.fixture
def mock_context_manager():
    return MagicMock(spec=ContextManager)

@pytest.fixture
def chat_service(mock_llm_service, mock_context_manager):
    return ChatService(mock_llm_service, mock_context_manager)

@pytest.mark.asyncio
async def test_process_message_returns_llm_response(chat_service, mock_llm_service, mock_context_manager):
    # Arrange
    test_message = "Hello, AI!"
    mock_response = "Any response here"
    mock_llm_service.generate_response.return_value = mock_response
    mock_context_manager.get_context.return_value = ["Previous context"]

    # Act
    result = await chat_service.process_message(test_message)

    # Assert
    assert isinstance(result, ChatResponse)
    assert result.response == mock_response
    assert len(result.response) > 0  # Ensure we got a non-empty response
    mock_context_manager.add_to_context.assert_any_call(f"User: {test_message}")
    mock_context_manager.add_to_context.assert_any_call(f"AI: {mock_response}")
    mock_llm_service.generate_response.assert_called_once()

@pytest.mark.asyncio
async def test_process_message_content(chat_service, mock_llm_service, mock_context_manager):
    # Arrange
    test_message = "Tell me about windows"
    mock_response = "Windows are essential components in building construction, providing light, ventilation, and views."
    mock_llm_service.generate_response.return_value = mock_response
    mock_context_manager.get_context.return_value = []

    # Act
    result = await chat_service.process_message(test_message)

    # Assert
    assert "window" in result.response.lower()
    assert len(result.response) > 20  # Ensure we got a substantial response

@pytest.mark.asyncio
async def test_generate_response_prompt(chat_service, mock_llm_service, mock_context_manager):
    # Arrange
    test_message = "Hello, AI!"
    mock_response = "Mock AI response"
    mock_context_manager.get_context.return_value = ["Previous context"]
    mock_llm_service.generate_response.return_value = mock_response

    # Act
    result = await chat_service.process_message(test_message)

    # Assert
    assert isinstance(result, ChatResponse)
    assert result.response == mock_response
    
    called_prompt = mock_llm_service.generate_response.call_args[0][0]
    
    # Check for key elements without exact wording
    assert any(word in called_prompt.lower() for word in ["assistant", "ai", "help"])
    assert "window" in called_prompt.lower() and "manufacturing" in called_prompt.lower()
    assert "Previous context" in called_prompt
    assert f"User: {test_message}" in called_prompt
    assert called_prompt.endswith("AI:")
    
    # Check overall structure
    prompt_lines = called_prompt.split("\n")
    assert len(prompt_lines) >= 5  # Ensure we have at least: system message, context intro, previous context, user message, and AI prompt
    assert prompt_lines[-2].startswith("User:")
    assert prompt_lines[-1] == "AI:"


def test_generate_prompt(chat_service, mock_context_manager):
    # Arrange
    test_message = "Tell me about double-pane windows"
    mock_context_manager.get_context.return_value = ["User: Hello", "AI: Hi there!"]

    # Act
    prompt = chat_service._generate_prompt(test_message)

    # Assert
    assert "window manufacturing" in prompt.lower()
    assert "User: Hello" in prompt
    assert "AI: Hi there!" in prompt
    assert f"User: {test_message}" in prompt
    assert prompt.endswith("AI:")
    
    # Check for overall structure
    assert prompt.count("User:") == 2  # One from context, one new
    assert prompt.count("AI:") == 2  # One from context, one for new response

@pytest.mark.asyncio
async def test_get_conversation_history(chat_service, mock_context_manager):
    # Arrange
    mock_context_manager.get_context.return_value = [
        "User: Hello",
        "AI: Hi there!",
        "User: Tell me about windows",
        "AI: Sure, I'd be happy to discuss windows."
    ]

    # Act
    history = await chat_service.get_conversation_history()

    # Assert
    assert history == [
        ("user", "Hello"),
        ("ai", "Hi there!"),
        ("user", "Tell me about windows"),
        ("ai", "Sure, I'd be happy to discuss windows.")
    ]

def test_clear_conversation(chat_service, mock_context_manager):
    # Act
    chat_service.clear_conversation()

    # Assert
    mock_context_manager.clear_context.assert_called_once()

@pytest.mark.asyncio
async def test_process_message_with_empty_context(chat_service, mock_llm_service, mock_context_manager):
    # Arrange
    test_message = "Hello, AI!"
    mock_response = "Mock response about window manufacturing"
    mock_llm_service.generate_response.return_value = mock_response
    mock_context_manager.get_context.return_value = []

    # Act
    result = await chat_service.process_message(test_message)

    # Assert
    assert result.response == mock_response
    mock_context_manager.get_context.assert_called_once()
    generated_prompt = mock_llm_service.generate_response.call_args[0][0]
    assert "User: Hello, AI!" in generated_prompt
    assert generated_prompt.count("User: ") == 1
    assert generated_prompt.count("AI:") == 1
    assert "window manufacturing" in generated_prompt.lower()

@pytest.mark.asyncio
async def test_process_message_error_handling(chat_service, mock_llm_service):
    # Arrange
    test_message = "Trigger an error"
    mock_llm_service.generate_response.side_effect = Exception("LLM service error")

    # Act & Assert
    with pytest.raises(Exception, match="LLM service error"):
        await chat_service.process_message(test_message)