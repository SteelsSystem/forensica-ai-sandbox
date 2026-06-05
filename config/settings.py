from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "development"
    cors_origins: List[str] = ["http://localhost:3000"]
    mistral_api_key: str = ""
    mistral_model_fast: str = "mistral-small-latest"
    mistral_model_deep: str = "mistral-large-latest"
    scaleway_secret_key: str = ""
    scaleway_inference_endpoint: str = "https://api.scaleway.ai/v1"
    database_url: str = "postgresql+asyncpg://forensica:password@localhost:5432/forensica_db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "dev-secret"
    encryption_key: str = "dev-encryption-key-32bytes-change"
    aml_threshold_eur: float = 15000.0
    data_retention_days: int = 730

settings = Settings()
