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
