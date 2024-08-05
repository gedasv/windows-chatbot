"""
This module defines the API routes for the chat functionality of the chatbot.
"""

# app/api/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from pydantic import BaseModel, Field
from typing import List, Tuple, Dict, Optional
from app.services.chat_service import ChatService
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.utils.context_manager import ContextManager

router = APIRouter()

llm_service = LLMService()
context_manager = ContextManager()
chat_service = ChatService(llm_service, context_manager)

class ErrorResponse(BaseModel):
    """
    Model for error responses.

    :param detail: A string describing the error.
    """
    detail: str

# class ConversationHistory(BaseModel):
#     history: List[Tuple[str, str]]

class ConversationHistory(BaseModel):
    """
    Model for conversation history with context information.

    :param history: A list of tuples containing the conversation history.
    :param context_info: A dictionary with information about the conversation context.
    """
    history: List[Tuple[str, str]]
    context_info: Optional[Dict[str, int]] = None

class ChatRequest(BaseModel):
    """
    Model for chat request.

    :param message: The user's input message, with length constraints.
    """
    message: str = Field(..., min_length=1, max_length=1000)

def get_chat_service():
    """
    Dependency injection function to get the ChatService instance.

    :return: An instance of ChatService.
    """
    return chat_service

@router.post("/chat", response_model=ChatResponse, responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def chat(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    """
    Endpoint for processing a chat message.

    :param request: The ChatRequest containing the user's message.
    :param chat_service: An instance of ChatService, injected as a dependency.
    :return: A ChatResponse containing the AI's response.
    :raises HTTPException: If the message is empty or an error occurs during processing.
    """
    stripped_message = request.message.strip()
    if not stripped_message:
        raise HTTPException(status_code=422, detail="Message cannot be empty or just whitespace")
    try:
        return await chat_service.process_message(stripped_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation", response_model=ConversationHistory, responses={500: {"model": ErrorResponse}})
async def get_conversation(
    include_context: Optional[bool] = Query(None, description="Include context information"),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Endpoint for retrieving the conversation history and optionally context information.

    :param include_context: If True, includes context information in the response.
    :param chat_service: An instance of ChatService, injected as a dependency.
    :return: A dictionary containing the conversation history and optionally context info.
    :raises HTTPException: If an error occurs while retrieving the conversation history.
    """
    try:
        history = await chat_service.get_conversation_history()
        response = {"history": history}

        if include_context:
            context_info = chat_service.get_context_info()
            response["context_info"] = context_info

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_conversation(chat_service: ChatService = Depends(get_chat_service)):
    """
    Endpoint for clearing the conversation history.

    :param chat_service: An instance of ChatService, injected as a dependency.
    :return: A Response with a 204 No Content status code on success.
    :raises HTTPException: If an error occurs while clearing the conversation.
    """
    try:
        chat_service.clear_conversation()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))