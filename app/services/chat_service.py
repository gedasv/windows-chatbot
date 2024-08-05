from app.services.llm_service import LLMService
from app.utils.context_manager import ContextManager
from app.models.chat_models import ChatResponse
from typing import List, Tuple, Dict

import logging
logger = logging.getLogger(__name__)

class ChatService:
    """
    A service class for managing chat interactions with an AI assistant.
    
    This class integrates the LLM service for generating responses and a context manager
    for maintaining conversation history.
    """
    def __init__(self, llm_service: LLMService, context_manager: ContextManager):
        """
        Initialize the ChatService with LLM service and context manager.

        :param llm_service: An instance of LLMService for generating AI responses.
        :param context_manager: An instance of ContextManager for maintaining conversation context.
        """
        self.llm_service = llm_service
        self.context_manager = context_manager

    async def process_message(self, message: str) -> ChatResponse:
        """
        Process a user message and generate an AI response.

        :param message: The user's input message.
        :return: A ChatResponse object containing the AI's response.
        """
        prompt = self._generate_prompt(message)
        llm_response = await self.llm_service.generate_response(prompt)

        self.context_manager.add_to_context(f"User: {message}")
        self.context_manager.add_to_context(f"AI: {llm_response}")

        return ChatResponse(response=llm_response)

    def _generate_prompt(self, message: str) -> str:
        """
        Generate a prompt for the LLM based on the current context and user message.

        :param message: The user's input message.
        :return: A string containing the generated prompt for the LLM.
        """
        context = self.context_manager.get_context()
        prompt_parts = [
            "You are a helpful AI assistant specializing in window manufacturing.",
            "Please provide accurate and helpful responses based on the conversation context.",
            "Here's the conversation so far:",
            *context,
            f"User: {message}",
            "AI:",
        ]
        return "\n".join(prompt_parts)

    async def get_conversation_history(self) -> List[Tuple[str, str]]:
        """
        Retrieve the conversation history from the context manager.

        :return: A list of tuples, each containing a speaker ('user' or 'ai') and their message.
        """
        context = self.context_manager.get_context()
        conversation = []
        for entry in context:
            if entry.startswith("User: "):
                conversation.append(("user", entry[6:]))
            elif entry.startswith("AI: "):
                conversation.append(("ai", entry[4:]))

        return conversation

    def clear_conversation(self) -> None:
        """ Clear the current conversation history from the context manager. """
        self.context_manager.clear_context()

    def get_context_info(self) -> Dict[str, int]:
        """
        Get information about the current context.

        :return: A dictionary containing the current and maximum context length.
        """
        return {
            "current_length": self.context_manager.get_context_length(),
            "max_length": self.context_manager.get_max_context_length()
        }