from typing import Dict, Any
from app.core.config import settings, Settings, BackendConfig
from app.services.backends.base import BaseBackend
from app.services.backends.echo_backend import EchoBackend
from app.services.backends.http_backend import HTTPBackend
from app.core.utils.token_usage import approx_tokens


class InferenceService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._backends: Dict[str, BaseBackend] = {}
        self._load_backends()
    
    def _load_backends(self):
        for name, config in self.settings.backends.items():
            if config.type == "echo":
                self._backends[name] = EchoBackend(name, config.model_dump())
            elif config.type == "http":
                self._backends[name] = HTTPBackend(name, config.model_dump())
            else:
                print(f"Warning: Unknown backend type '{config.type}' for '{name}'")
    
    def _get_backend(self, model_name: str) -> tuple[BaseBackend, str]:
        if model_name and model_name in self._backends:
            return self._backends[model_name], model_name
        
        default = self.settings.default_backend
        if default in self._backends:
            return self._backends[default], default
        
        if "echo" not in self._backends:
            self._backends["echo"] = EchoBackend("echo", {})
        return self._backends["echo"], "echo"
    
    async def process_inference(
        self, 
        payload: Dict[str, Any], 
        prompt: str, 
        request_id: str
    ) -> Dict[str, Any]:
        model_name = payload.get("model", "")
        backend, backend_name = self._get_backend(model_name)
        reply = await backend.generate(prompt, payload, request_id)
        
        pt = approx_tokens(prompt)
        ct = approx_tokens(reply)
        
        return {
            "id": request_id,
            "backend": backend_name,
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
