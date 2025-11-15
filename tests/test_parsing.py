"""Tests for parsing utilities."""
import pytest
from app.parsing import parse_question


def test_parse_question():
    """Test basic question parsing."""
    result = parse_question("What is the weather?")
    
    assert result["raw"] == "What is the weather?"
    assert result["intent"] in ["what", "when", "how_many", "unknown"]
    assert result["topic"] in ["trip", "cars", "restaurants", "general"]


def test_parse_empty_question():
    """Test parsing an empty question."""
    result = parse_question("")
    
    assert result["raw"] == ""
    assert result["intent"] in ["what", "when", "how_many", "unknown"]


def test_parse_how_many_question():
    """Test parsing a 'how many' question."""
    result = parse_question("How many cars does John have?")
    
    assert result["intent"] == "how_many"
    assert result["topic"] == "cars"
    assert "John" in (result["member_name"] or "")


def test_parse_when_question():
    """Test parsing a 'when' question."""
    result = parse_question("When is Layla's trip?")
    
    assert result["intent"] == "when"
    assert "Layla" in (result["member_name"] or "")


def test_parse_restaurant_question():
    """Test parsing a restaurant question."""
    result = parse_question("What restaurants does Vikram like?")
    
    assert result["topic"] == "restaurants"
    assert "Vikram" in (result["member_name"] or "")
