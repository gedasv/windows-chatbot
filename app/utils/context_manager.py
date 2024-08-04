# app/utils/context_manager.py
from collections import deque
from typing import List, Optional

class ContextManager:
    def __init__(self, max_context_length: int = 10):
        """
        Initialize the ContextManager with a fixed-size circular buffer.
        
        Args:
            max_context_length (int): Maximum number of messages to keep in context.
        """
        self.max_context_length = max_context_length
        self.context = deque(maxlen=max_context_length)

    def add_to_context(self, message: str) -> None:
        """
        Add a message to the context.
        
        Args:
            message (str): The message to add to the context.
        """
        self.context.append(message)

    def get_context(self) -> List[str]:
        """
        Retrieve the current context as a list of messages.
        
        Returns:
            List[str]: The current context messages.
        """
        return list(self.context)

    def get_context_string(self, separator: str = "\n") -> str:
        """
        Retrieve the current context as a single string.
        
        Args:
            separator (str): The string to use for joining context messages.
        
        Returns:
            str: The current context as a single string.
        """
        return separator.join(self.context)

    def clear_context(self) -> None:
        """Clear all messages from the context."""
        self.context.clear()

    def get_context_length(self) -> int:
        """
        Get the current number of messages in the context.
        
        Returns:
            int: The number of messages in the context.
        """
        return len(self.context)

    def get_last_message(self) -> Optional[str]:
        """
        Get the last message added to the context.
        
        Returns:
            Optional[str]: The last message, or None if the context is empty.
        """
        return self.context[-1] if self.context else None