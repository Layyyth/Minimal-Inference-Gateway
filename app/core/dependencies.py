from app.core.config import settings, Settings
from app.services.inference import InferenceService


def get_settings() -> Settings:
    return settings


def get_inference_service() -> InferenceService:
    return InferenceService(settings=settings)
