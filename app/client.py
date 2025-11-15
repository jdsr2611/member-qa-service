from typing import Any, Dict, List
import httpx


class MessagesClient:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get_messages(self, parsed_question: Dict[str, Any]) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/messages"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        # Adjust if the API wraps messages differently
        if isinstance(data, dict) and "messages" in data:
            return data["messages"]
        if isinstance(data, list):
            return data
        return []
