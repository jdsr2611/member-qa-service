from typing import Dict, List
import re


def _extract_dates(text: str) -> List[str]:
    dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
    dates += re.findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}\b", text)
    return dates


def answer_from_messages(question: str, parsed: Dict, messages: List[Dict]) -> str:
    intent = parsed.get("intent")
    topic = parsed.get("topic")
    member_name = parsed.get("member_name") or "This member"

    if not messages:
        return "I couldn't find that information in the member messages."

    texts = [str(m.get("text", "")) for m in messages]

    if intent == "how_many" and topic == "cars":
        car_count = None
        for t in texts:
            m = re.search(r"\b(\d+)\s+cars?\b", t.lower())
            if m:
                car_count = int(m.group(1))
                break
        if car_count is not None:
            return f"{member_name} has {car_count} car(s)."
        mention_count = sum("car" in t.lower() for t in texts)
        if mention_count > 0:
            return f"I see multiple mentions of cars for {member_name}, but not a clear count."
        return "I couldn't determine how many cars they have from the messages."

    if intent == "when" and topic == "trip":
        for t in texts:
            if "trip" in t.lower() or "travel" in t.lower():
                dates = _extract_dates(t)
                if dates:
                    if len(dates) == 1:
                        return f"{member_name} is planning their trip around {dates[0]}."
                    elif len(dates) >= 2:
                        return f"{member_name} is planning their trip from {dates[0]} to {dates[1]}."
                return f"I found this about {member_name}'s trip: \"{t}\""
        return "I couldn't find when the trip is planned."

    if intent == "what" and topic == "restaurants":
        restaurants = set()
        for t in texts:
            if "favorite" in t.lower() and "restaurant" in t.lower():
                part = re.split(r"are|is|:", t, maxsplit=1)
                if len(part) > 1:
                    names_raw = part[1]
                    for name in re.split(r",|and", names_raw):
                        n = name.strip(" .!?")
                        if len(n) > 1:
                            restaurants.add(n)
        if restaurants:
            rest_str = ", ".join(sorted(restaurants))
            return f"{member_name}'s favorite restaurants are: {rest_str}."
        return "I couldn't find a clear list of favorite restaurants."

    top = texts[0]
    return f"I found this related message: \"{top}\""
