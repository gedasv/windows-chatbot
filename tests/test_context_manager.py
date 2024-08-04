import pytest
from app.utils.context_manager import ContextManager

@pytest.fixture
def context_manager():
    return ContextManager(max_context_length=5)

def test_add_to_context(context_manager):
    context_manager.add_to_context("Hello")
    assert context_manager.get_context() == ["Hello"]

def test_get_context(context_manager):
    messages = ["Hello", "World", "Test"]
    for msg in messages:
        context_manager.add_to_context(msg)
    assert context_manager.get_context() == messages

def test_get_context_string(context_manager):
    messages = ["Hello", "World", "Test"]
    for msg in messages:
        context_manager.add_to_context(msg)
    assert context_manager.get_context_string() == "Hello\nWorld\nTest"
    assert context_manager.get_context_string(separator=" ") == "Hello World Test"

def test_clear_context(context_manager):
    context_manager.add_to_context("Test")
    context_manager.clear_context()
    assert context_manager.get_context() == []

def test_get_context_length(context_manager):
    messages = ["Hello", "World", "Test"]
    for msg in messages:
        context_manager.add_to_context(msg)
    assert context_manager.get_context_length() == 3

def test_get_last_message(context_manager):
    messages = ["Hello", "World", "Test"]
    for msg in messages:
        context_manager.add_to_context(msg)
    assert context_manager.get_last_message() == "Test"

def test_max_context_length(context_manager):
    messages = ["1", "2", "3", "4", "5", "6", "7"]
    for msg in messages:
        context_manager.add_to_context(msg)
    assert context_manager.get_context() == ["3", "4", "5", "6", "7"]
    assert context_manager.get_context_length() == 5

def test_empty_context(context_manager):
    assert context_manager.get_context() == []
    assert context_manager.get_context_string() == ""
    assert context_manager.get_context_length() == 0
    assert context_manager.get_last_message() is None

def test_custom_max_length():
    custom_manager = ContextManager(max_context_length=3)
    messages = ["1", "2", "3", "4", "5"]
    for msg in messages:
        custom_manager.add_to_context(msg)
    assert custom_manager.get_context() == ["3", "4", "5"]
    assert custom_manager.get_context_length() == 3