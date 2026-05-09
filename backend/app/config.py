from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Clerk
    clerk_secret_key: str = ""
    clerk_publishable_key: str = ""

    # Zendesk (Signal's OAuth app credentials — registered once at developer.zendesk.com)
    zendesk_client_id: str = ""
    zendesk_client_secret: str = ""

    # OpenAI (embeddings)
    openai_api_key: str = ""

    # Anthropic
    anthropic_api_key: str = ""

    # App
    environment: str = "development"
    debug: bool = False
    frontend_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
