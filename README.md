# Member Question-Answering Service

This project implements a small HTTP API that answers natural-language questions about members, using the public `GET /messages` endpoint provided in the assignment.

Examples of supported questions:

- “When is Layla planning her trip to London?”
- “How many cars does Vikram Desai have?”
- “What are Amira’s favorite restaurants?”

The core behaviour:

```http
POST /ask
Content-Type: application/json

{ "question": "When is Layla planning her trip to London?" }

200 OK
{ "answer": "Layla is planning her trip from 2025-03-10 to 2025-03-15." }
