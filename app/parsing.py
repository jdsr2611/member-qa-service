from typing import Dict
import re


def parse_question(question: str) -> Dict:
    q = question.strip()
    q_lower = q.lower()

    if "how many" in q_lower or "number of" in q_lower:
        intent = "how_many"
    elif "when" in q_lower:
        intent = "when"
    elif "what" in q_lower:
        intent = "what"
    else:
        intent = "unknown"

    if "trip" in q_lower or "travel" in q_lower:
        topic = "trip"
    elif "car" in q_lower or "cars" in q_lower:
        topic = "cars"
    elif "restaurant" in q_lower or "restaurants" in q_lower:
        topic = "restaurants"
    else:
        topic = "general"

    name_pattern = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b", q)
    member_name = " ".join(name_pattern) if name_pattern else None

    return {
        "raw": q,
        "intent": intent,
        "topic": topic,
        "member_name": member_name,
    }
