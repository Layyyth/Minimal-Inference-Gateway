import os
import secrets
from pydantic import BaseModel, Field

def load_env_file():
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

class Settings(BaseModel):
    PROJECT_NAME: str = "MinimalInferenceGateWay"
    PORT: int = Field(default=8080, validation_alias="PORT")
    HOST: str = "0.0.0.0"
    
    BACKEND_URL: str = Field(default="", validation_alias="BACKEND_URL")
    BACKEND_TIMEOUT: float = Field(default=60.0, validation_alias="BACKEND_TIMEOUT")
    
    @property
    def backend_enabled(self) -> bool:
        return bool(self.BACKEND_URL.strip())

def get_settings() -> Settings:
    return Settings(
        PORT=int(os.getenv("PORT", 8080)),
        BACKEND_URL=os.getenv("BACKEND_URL", "").strip(),
        BACKEND_TIMEOUT=float(os.getenv("BACKEND_TIMEOUT", 60.0)),
    )

settings = get_settings()
