from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EDEN Witness Companion API"
    env: str = "dev"
    database_url: str = "sqlite:///./iota_witness.db"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_timeout_seconds: float = 15.0
    openai_max_retries: int = 2
    log_raw_text: bool = False
    data_retention_days: int = 0
    store_eden_text: bool = False
    privacy_policy_url: str = "http://localhost:8000/v1/privacy"
    terms_url: str = "http://localhost:8000/v1/terms"
    contact_email: str = "support@example.com"
    logos_api_key: str | None = None
    logos_base_url: str = "https://api.faithlife.com/v3"
    narrative_redis_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="IOTA_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
