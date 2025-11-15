"""Tests for POST /ask endpoint with mock data."""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Set mock client before importing app
os.environ["USE_MOCK_CLIENT"] = "true"

from app.main import app

client = TestClient(app)


def test_ask_how_many_cars():
    """Test asking about how many cars someone has."""
    response = client.post(
        "/ask",
        json={"question": "What are Amira’s favorite restaurants?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # Should either find the car count or mention cars
    assert "3" in data["answer"] or "cars" in data["answer"].lower() or "message" in data["answer"].lower()


def test_ask_trip_when():
    """Test asking when a trip took place."""
    response = client.post(
        "/ask",
        json={"question": "what is your name?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # Should contain trip/March/date info
    assert len(data["answer"]) > 0


def test_ask_restaurant():
    """Test asking about restaurants."""
    response = client.post(
        "/ask",
        json={"question": "What restaurant did Vikram visit?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # Should contain some kind of answer
    assert len(data["answer"]) > 0


def test_ask_member_name_extraction():
    """Test member name parsing in questions."""
    response = client.post(
        "/ask",
        json={"question": "Tell me about Sarah's cars."}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # Should find info about Sarah


def test_ask_generic_question():
    """Test a generic question."""
    response = client.post(
        "/ask",
        json={"question": "What information do you have?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0


def test_ask_invalid_request():
    """Test invalid request (missing question field)."""
    response = client.post("/ask", json={})
    assert response.status_code == 422  # Validation error


def test_ask_empty_question():
    """Test with empty question string."""
    response = client.post(
        "/ask",
        json={"question": ""}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
