from fastapi import FastAPI
from pydantic import BaseModel

from .client import MessagesClient
from .parsing import parse_question
from .retrieval import retrieve_relevant_messages
from .answering import answer_from_messages

app = FastAPI(title="Member QA Service")


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


messages_client = MessagesClient(
    base_url="https://november7-730026606190.europe-west1.run.app"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.post("/ask", response_model=AnswerResponse)
async def ask(payload: QuestionRequest):
    question = payload.question
    parsed = parse_question(question)

    try:
        messages = await messages_client.get_messages(parsed)
    except Exception as e:
        print("Error fetching messages:", e)
        messages = []

    relevant = retrieve_relevant_messages(parsed, messages)
    answer = answer_from_messages(question, parsed, relevant)
    return AnswerResponse(answer=answer)
