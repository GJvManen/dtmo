from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DTMO_",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Literal["development", "test", "staging", "production"] = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://dtmo:dtmo@postgres:5432/dtmo"
    redis_url: str = "redis://redis:6379/0"
    opensearch_url: str = "http://opensearch:9200"
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "dtmo"
    minio_secret_key: SecretStr = SecretStr("change-me")
    connector_poll_seconds: int = Field(default=3600, ge=60)
    connector_timeout_seconds: int = Field(default=30, ge=1, le=300)
    connector_max_attempts: int = Field(default=4, ge=1, le=10)
    publish_requires_human_approval: bool = True
    feature_live_connectors: bool = False
    feature_ai_analyst: bool = False

    @property
    def production(self) -> bool:
        return self.environment == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
