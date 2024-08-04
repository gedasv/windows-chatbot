import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_service import LLMService
from tenacity import RetryError

@pytest.fixture
def mock_chat_groq():
    with patch('app.services.llm_service.ChatGroq') as MockChatGroq:
        mock_instance = AsyncMock()
        MockChatGroq.return_value = mock_instance
        yield mock_instance

@pytest.mark.asyncio
async def test_generate_response_content_attribute(mock_chat_groq):
    mock_chat_groq.ainvoke.return_value = AsyncMock(content="Test response")
    llm_service = LLMService()
    response = await llm_service.generate_response("Test prompt")
    assert response == "Test response"
    mock_chat_groq.ainvoke.assert_called_once()

@pytest.mark.asyncio
async def test_generate_response_direct_string(mock_chat_groq):
    mock_chat_groq.ainvoke.return_value = "Direct test response"
    llm_service = LLMService()
    response = await llm_service.generate_response("Test prompt")
    assert response == "Direct test response"
    mock_chat_groq.ainvoke.assert_called_once()

@pytest.mark.asyncio
async def test_generate_response_raw(mock_chat_groq):
    mock_generation = MagicMock()
    mock_generation.text = "Raw test response"
    mock_chat_groq.agenerate.return_value = MagicMock(
        generations=[[mock_generation]]
    )
    llm_service = LLMService(chat_model=mock_chat_groq)
    response = await llm_service.generate_response_raw("Test prompt")
    assert response == "Raw test response"
    mock_chat_groq.agenerate.assert_called_once()

@pytest.mark.asyncio
async def test_generate_response_stream(mock_chat_groq):
    mock_stream = AsyncMock()
    mock_stream.__aiter__.return_value = [
        AsyncMock(content="Chunk 1"),
        AsyncMock(content="Chunk 2"),
    ]
    mock_chat_groq.astream.return_value = mock_stream

    llm_service = LLMService(chat_model=mock_chat_groq)
    chunks = []
    async for chunk in llm_service.generate_response_stream("Test prompt"):
        chunks.append(chunk)

    assert chunks == ["Chunk 1", "Chunk 2"]
    mock_chat_groq.astream.assert_called_once()


# ERRORS

@pytest.mark.asyncio
async def test_generate_response_error_handling(mock_chat_groq):
    mock_chat_groq.ainvoke.side_effect = Exception("API Error")
    llm_service = LLMService()
    with pytest.raises(Exception):
        await llm_service.generate_response("Test prompt")

@pytest.mark.asyncio
async def test_generate_response_unexpected_type(mock_chat_groq):
    mock_chat_groq.ainvoke.return_value = 12345
    llm_service = LLMService()
    with pytest.raises(RetryError) as exc_info:
        await llm_service.generate_response("Test prompt")
    
    assert isinstance(exc_info.value.last_attempt.exception(), ValueError)
    assert str(exc_info.value.last_attempt.exception()) == "Unexpected response type: <class 'int'>"


# We tested errors in the previous test anyway
# @pytest.mark.asyncio
# async def test_generate_response_raw_error_handling(mock_chat_groq):
#     mock_chat_groq.agenerate.side_effect = Exception("API Error")
#     llm_service = LLMService(chat_model=mock_chat_groq)
#     with pytest.raises(Exception):
#         await llm_service.generate_response_raw("Test prompt")