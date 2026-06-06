from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent AI Workflow Platform"
    environment: str = "development"
    api_key: str = "dev-api-key"
    enable_api_key_auth: bool = True
    database_url: str = "sqlite+aiosqlite:///./multi_agent_ai.db"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_knowledge"
    log_level: str = "INFO"
    default_provider: str = "local"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
