from typing import Any, Dict, List
import httpx



class MessagesClient:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get_messages(self, parsed_question: Dict[str, Any]) -> List[Dict[str, Any]]:
        # TEMP: hard-coded dummy data so /ask always works
        return [
            {
                "member_name": "Layla",
                "text": "Layla is planning her trip to London from 2025-03-10 to 2025-03-15."
            },
            {
                "member_name": "Vikram Desai",
                "text": "Vikram owns 2 cars and a bike."
            },
            {
                "member_name": "Amira",
                "text": "Amira's favorite restaurants are Olive Bistro, Spice Route and Cafe Noir."
            },
        ]
