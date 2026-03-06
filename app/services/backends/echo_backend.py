from typing import Dict, Any
from app.services.backends.base import BaseBackend


class EchoBackend(BaseBackend):
    async def generate(self, prompt: str, payload: Dict[str, Any], request_id: str) -> str:
        return f"Echo: {prompt}"
