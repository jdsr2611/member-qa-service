"""Tests for answer extraction logic."""
import pytest
from app.answering import answer_from_messages


def test_answer_from_messages_how_many():
    """Test answer extraction for 'how many' questions."""
    parsed = {
        "raw": "How many cars?",
        "intent": "how_many",
        "topic": "cars",
        "member_name": "John",
    }
    messages = [
        {"text": "John has 3 cars."},
        {"text": "He drives them often."},
    ]
    
    answer = answer_from_messages("How many cars?", parsed, messages)
    assert "3" in answer or "cars" in answer.lower()


def test_answer_from_messages_no_messages():
    """Test answer extraction with no relevant messages."""
    parsed = {
        "raw": "What?",
        "intent": "unknown",
        "topic": "general",
        "member_name": None,
    }
    messages = []
    
    answer = answer_from_messages("What?", parsed, messages)
    assert "couldn't find" in answer.lower()


def test_answer_from_messages_fallback():
    """Test fallback answer using first message."""
    parsed = {
        "raw": "Tell me something",
        "intent": "unknown",
        "topic": "general",
        "member_name": None,
    }
    messages = [
        {"text": "This is a sample message."},
    ]
    
    answer = answer_from_messages("Tell me something", parsed, messages)
    assert "sample message" in answer
