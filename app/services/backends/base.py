from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseBackend(ABC):
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
    
    @abstractmethod
    async def generate(self, prompt: str, payload: Dict[str, Any], request_id: str) -> str:
        pass
