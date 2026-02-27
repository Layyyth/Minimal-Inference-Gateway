import httpx
from typing import Dict, Any, Optional
from app.core.config import Settings

class BackendClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = self.settings.BACKEND_URL.rstrip("/")
        self.timeout = httpx.Timeout(self.settings.BACKEND_TIMEOUT)

    async def forward_to_backend(self, payload: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": request_id,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Backend returned error status {e.response.status_code}: {e.response.text}")
            except httpx.RequestException as e:
                raise Exception(f"Backend request failed: {e}")

    def extract_reply(self, backend_json: Dict[str, Any]) -> str:
        try:
            return backend_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return str(backend_json)
