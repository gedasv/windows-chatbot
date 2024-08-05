# app/services/llm_service.py
from typing import AsyncGenerator
from app.config import settings
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class LLMService:
    """
    A service class for interacting with the Groq language model.

    This class provides methods to generate responses using the Groq API,
    including standard responses, raw responses, and streaming responses.
    Raw responses and streaming responses were used for testing purposes,
    but are not used in the app.

    :param chat_model: An optional ChatGroq instance to use instead of creating a new one.
    :param max_retries: Maximum number of retries for API calls.
    :param timeout: Timeout for API calls in seconds.
    :param model_params: Additional parameters to pass to the ChatGroq constructor.
    """
    def __init__(self, chat_model=None, max_retries=3, timeout=30, **model_params):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = settings.MODEL_NAME
        self.max_retries = max_retries
        self.timeout = timeout
        self.groq_chat = chat_model or ChatGroq(
            groq_api_key=self.api_key,
            model_name=self.model,
            max_retries=self.max_retries,
            timeout=self.timeout,
            **model_params
        )
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate_response(self, prompt: str, system_prompt: str = "You are a helpful assistant specializing in window manufacturing.", **kwargs) -> str:
        """
        Generate a response using the Groq chat model.

        This method uses retry logic to handle potential failures.

        :param prompt: The user's input prompt.
        :param system_prompt: The system prompt to set the context for the AI.
        :param kwargs: Additional keyword arguments to pass to the chat model.
        :return: The generated response as a string.
        :raises ValueError: If the response type is unexpected.
        """
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ]
        response = await self.groq_chat.ainvoke(messages, **kwargs)
        if hasattr(response, 'content'):
            return response.content.strip()
        elif isinstance(response, str):
            return response.strip()
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate_response_raw(self, prompt: str, system_prompt: str = "You are a helpful assistant specializing in window manufacturing.", **kwargs) -> str:
        """
        Generate a raw response using the Groq chat model.

        This method returns the raw text from the model's response.

        :param prompt: The user's input prompt.
        :param system_prompt: The system prompt to set the context for the AI.
        :param kwargs: Additional keyword arguments to pass to the chat model.
        :return: The raw generated response as a string.
        """
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ]
        response = await self.groq_chat.agenerate([messages], **kwargs)
        return response.generations[0][0].text.strip()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate_response_stream(self, prompt: str, system_prompt: str = "You are a helpful assistant specializing in window manufacturing.", **kwargs) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response using the Groq chat model.

        This method returns an asynchronous generator that yields response chunks.

        :param prompt: The user's input prompt.
        :param system_prompt: The system prompt to set the context for the AI.
        :param kwargs: Additional keyword arguments to pass to the chat model.
        :return: An asynchronous generator yielding response chunks.
        """
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ]
        stream = await self.groq_chat.astream(messages, **kwargs)
        async for chunk in stream:
            if chunk.content:
                yield chunk.content