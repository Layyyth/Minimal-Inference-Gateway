from typing import Dict, Any
from app.core.config import settings, Settings
from app.services.backend_client import BackendClient
from app.services.echo_service import echo_reply
from app.core.utils.token_usage import approx_tokens

class InferenceService:
    def __init__(self, settings: Settings, backend_client: BackendClient):
        self.settings = settings
        self.backend_client = backend_client

    async def process_inference(self, payload: Dict[str, Any], prompt: str, request_id: str) -> Dict[str, Any]:
        if self.settings.backend_enabled:
            backend_json = await self.backend_client.forward_to_backend(payload, request_id)
            reply = self.backend_client.extract_reply(backend_json)
        else:
            reply = echo_reply(prompt)
        
        pt = approx_tokens(prompt)
        ct = approx_tokens(reply)
        
        return {
            "id": request_id,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": reply},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": pt,
                "completion_tokens": ct,
                "total_tokens": pt + ct
            },
        }
