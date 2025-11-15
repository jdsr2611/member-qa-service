from typing import Dict, List


def _normalize(s: str) -> str:
    return s.lower().strip()


def _matches_member_name(msg: Dict, member_name: str) -> bool:
    if not member_name:
        return True

    target = _normalize(member_name)
    fields = [
        msg.get("member_name"),
        msg.get("sender_name"),
        msg.get("from"),
        msg.get("to"),
        msg.get("text"),
    ]
    for f in fields:
        if isinstance(f, str) and target in _normalize(f):
            return True
    return False


def _matches_topic(msg: Dict, topic: str) -> bool:
    if topic == "general":
        return True
    text = _normalize(str(msg.get("text", "")))
    if topic == "trip":
        return any(k in text for k in ["trip", "travel", "flight", "hotel", "london"])
    if topic == "cars":
        return any(k in text for k in ["car", "cars", "vehicle", "garage"])
    if topic == "restaurants":
        return any(k in text for k in ["restaurant", "restaurants", "dinner", "brunch", "food"])
    return True


def retrieve_relevant_messages(parsed: Dict, messages: List[Dict]) -> List[Dict]:
    member_name = parsed.get("member_name")
    topic = parsed.get("topic", "general")

    filtered = [
        m for m in messages
        if _matches_member_name(m, member_name) and _matches_topic(m, topic)
    ]
    return filtered[:20]
