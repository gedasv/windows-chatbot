from app.services.llm_service import LLMService
from app.utils.context_manager import ContextManager
from app.models.chat_models import ChatResponse
from typing import List, Tuple

import logging
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, llm_service: LLMService, context_manager: ContextManager):
        self.llm_service = llm_service
        self.context_manager = context_manager

    async def process_message(self, message: str) -> ChatResponse:
        self.context_manager.add_to_context(f"User: {message}")

        prompt = self._generate_prompt(message)

        llm_response = await self.llm_service.generate_response(prompt)

        self.context_manager.add_to_context(f"AI: {llm_response}")

        return ChatResponse(response=llm_response)

    def _generate_prompt(self, message: str) -> str:
        context = self.context_manager.get_context()
        prompt_parts = [
            "You are a helpful AI assistant specializing in window manufacturing.",
            "Please provide accurate and helpful responses based on the conversation context.",
            "Here's the conversation so far:",
            *context,
            f"User: {message}",
            "AI:"
        ]
        return "\n".join(prompt_parts)

    async def get_conversation_history(self) -> List[Tuple[str, str]]:
        context = self.context_manager.get_context()
        conversation = []
        for entry in context:
            if entry.startswith("User: "):
                conversation.append(("user", entry[6:]))
            elif entry.startswith("AI: "):
                conversation.append(("ai", entry[4:]))
        # logger.info(f"Current context (in get_conversation_history()): {context}")
        # logger.info(f"Conversation history: {conversation}")
        return conversation

    def clear_conversation(self) -> None:
        self.context_manager.clear_context()