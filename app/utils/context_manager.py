# app/utils/context_manager.py
from collections import deque
from typing import List, Optional

class ContextManager:
    """
    Manages conversation context using a fixed-size circular buffer.

    This class provides methods to add, retrieve, and manipulate the conversation context.
    """
    def __init__(self, max_context_length: int = 10):
        """
        Initialize the ContextManager with a fixed-size circular buffer.

        :param max_context_length: Maximum number of messages to keep in context.
        """
        self.max_context_length = max_context_length
        self.context = deque(maxlen=max_context_length)

    def add_to_context(self, message: str) -> None:
        """
        Add a message to the context.

        :param message: The message to add to the context.
        """
        self.context.append(message)

    def get_context(self) -> List[str]:
        """
        Retrieve the current context as a list of messages.

        :return: The current context messages.
        """
        return list(self.context)

    def get_context_string(self, separator: str = "\n") -> str:
        """
        Retrieve the current context as a single string.

        :param separator: The string to use for joining context messages.
        :return: The current context as a single string.
        """
        return separator.join(self.context)

    def clear_context(self) -> None:
        """Clear all messages from the context."""
        self.context.clear()

    def get_context_length(self) -> int:
        """
        Get the current number of messages in the context.

        :return: The number of messages in the context.
        """
        return len(self.context)

    def get_last_message(self) -> Optional[str]:
        """
        Get the last message added to the context.

        :return: The last message, or None if the context is empty.
        """
        return self.context[-1] if self.context else None
    
    def get_max_context_length(self) -> int:
        """
        Get the maximum number of messages that can be stored in the context.

        :return: The maximum context length.
        """
        return self.max_context_length