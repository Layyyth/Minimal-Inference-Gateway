from fastapi import APIRouter
from app.api.v1.endpoints import chat_completion

api_router = APIRouter()
api_router.include_router(chat_completion.router, prefix="/chat", tags=["chat"])
