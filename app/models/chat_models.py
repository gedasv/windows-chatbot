"""
This module defines the Pydantic models for chat requests and responses.

These models are used for data validation and serialization in the chat API.
"""

# app/models/chat_models.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Model for a chat request."""
    message: str

class ChatResponse(BaseModel):
    """Model for a chat response."""
    response: str