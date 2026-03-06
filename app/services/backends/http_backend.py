import httpx
from typing import Dict, Any
from app.services.backends.base import BaseBackend


class HTTPBackend(BaseBackend):
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.url = config.get("url", "").rstrip("/")
        self.timeout = config.get("timeout", 60.0)
    
    async def generate(self, prompt: str, payload: Dict[str, Any], request_id: str) -> str:
        url = f"{self.url}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": request_id,
        }
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout)) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                backend_json = response.json()
                return self._extract_reply(backend_json)
            except httpx.HTTPStatusError as e:
                raise Exception(f"Backend '{self.name}' returned error status {e.response.status_code}: {e.response.text}")
            except httpx.ConnectError as e:
                raise Exception(f"Backend '{self.name}' connection failed: {e}")
            except Exception as e:
                raise Exception(f"Backend '{self.name}' request failed: {e}")
    
    def _extract_reply(self, backend_json: Dict[str, Any]) -> str:
        try:
            return backend_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return str(backend_json)
