import uuid
from typing import List, Dict, Any, Optional
from fastapi import Request

def get_request_id(request: Request) -> str:
    rid = request.headers.get("x-request-id") or request.headers.get("request-id")
    return rid if rid else str(uuid.uuid4())