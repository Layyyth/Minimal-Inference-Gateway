import os
import yaml
from typing import Dict, Any, List
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


class BackendConfig(BaseModel):
    name: str
    type: str
    url: str = ""
    timeout: float = 60.0


class Settings(BaseModel):
    PROJECT_NAME: str = "MinimalInferenceGateWay"
    PORT: int = Field(default=8080, validation_alias="PORT")
    HOST: str = "0.0.0.0"
    CONFIG_FILE: str = Field(default="config.yaml", validation_alias="CONFIG_FILE")
    backends: Dict[str, BackendConfig] = {}
    default_backend: str = "echo"


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    if not os.path.exists(config_path):
        return {}
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Warning: Failed to load config file {config_path}: {e}")
        return {}


def get_settings() -> Settings:
    config_file = os.getenv("CONFIG_FILE", "config.yaml")
    yaml_config = load_yaml_config(config_file)
    
    backends = {}
    for backend_data in yaml_config.get("backends", []):
        backend = BackendConfig(**backend_data)
        backends[backend.name] = backend
    
    if not backends:
        backends["echo"] = BackendConfig(name="echo", type="echo")
    
    return Settings(
        PORT=int(os.getenv("PORT", 8080)),
        HOST=os.getenv("HOST", "0.0.0.0"),
        CONFIG_FILE=config_file,
        backends=backends,
        default_backend=yaml_config.get("default_backend", "echo"),
    )


settings = get_settings()
