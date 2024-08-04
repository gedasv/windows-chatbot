# app/api/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
# from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Tuple
from app.services.chat_service import ChatService
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.utils.context_manager import ContextManager

router = APIRouter()

llm_service = LLMService()
context_manager = ContextManager()
chat_service = ChatService(llm_service, context_manager)

class ErrorResponse(BaseModel):
    detail: str

class ConversationHistory(BaseModel):
    history: List[Tuple[str, str]]

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

def get_chat_service():
    return chat_service

@router.post("/chat", response_model=ChatResponse, responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def chat(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    stripped_message = request.message.strip()
    if not stripped_message:
        raise HTTPException(status_code=422, detail="Message cannot be empty or just whitespace")
    try:
        return await chat_service.process_message(stripped_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation", response_model=ConversationHistory, responses={500: {"model": ErrorResponse}})
async def get_conversation(chat_service: ChatService = Depends(get_chat_service)):
    try:
        history = await chat_service.get_conversation_history()
        return ConversationHistory(history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_conversation(chat_service: ChatService = Depends(get_chat_service)):
    try:
        chat_service.clear_conversation()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))