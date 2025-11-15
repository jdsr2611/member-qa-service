from fastapi import FastAPI
from pydantic import BaseModel

from .client import MessagesClient
from .parsing import parse_question
from .retrieval import retrieve_relevant_messages
from .answering import answer_from_messages


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


# FastAPI app
app = FastAPI(title="Member QA Service")


# Messages client using the given public API
messages_client = MessagesClient(
    base_url="https://november7-730026606190.europe-west1.run.app"
)


@app.get("/")
def root():
    """
    Simple root endpoint so the base URL doesn't 404.
    """
    return {
        "message": "Member QA Service is running. Use POST /ask to ask a question."
    }


@app.get("/health")
def health_check():
    """
    Basic health check for uptime monitoring.
    """
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
async def ask(payload: QuestionRequest):
    """
    Main question-answering endpoint.

    Request:
    {
      "question": "When is Layla planning her trip to London?"
    }

    Response:
    {
      "answer": "..."
    }
    """
    question = payload.question

    # 1) Parse question (intent, topic, member name, etc.)
    parsed = parse_question(question)

    # 2) Fetch messages from external API (with safe fallback)
    try:
        messages = await messages_client.get_messages(parsed)
    except Exception as e:
        # Don't crash if the external API has an issue
        print("Error fetching messages from /messages API:", e)
        messages = []

    # 3) Retrieve relevant messages
    relevant = retrieve_relevant_messages(parsed, messages)

    # 4) Generate an answer
    answer = answer_from_messages(question, parsed, relevant)

    return AnswerResponse(answer=answer)
