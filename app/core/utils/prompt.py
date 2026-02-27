from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status

def extract_last_user_prompt(messages: List[Dict[str, Any]]) -> str:
    if not isinstance(messages, list) or not messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid messages format or missing prompt"
        )
    
    for m in reversed(messages):
        if isinstance(m, dict) and m.get("role") == "user":
            content = (m.get("content") or "").strip()
            if not content:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="User message content is empty"
                )
            return content
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="No valid user message found"
    )
