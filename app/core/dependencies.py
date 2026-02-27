from app.core.config import settings, Settings
from app.services.backend_client import BackendClient
from app.services.inference import InferenceService

def get_settings() -> Settings:
    return settings

def get_backend_client() -> BackendClient:
    return BackendClient(settings=settings)

def get_inference_service() -> InferenceService:
    return InferenceService(
        settings=settings,
        backend_client=get_backend_client()
    )
