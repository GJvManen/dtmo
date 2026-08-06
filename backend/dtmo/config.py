from __future__ import annotations

from functools import lru_cache
from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DTMO_", case_sensitive=False, extra="ignore")

    environment: Literal["development", "test", "staging", "production"] = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://dtmo@postgres:5432/dtmo"
    redis_url: str = "redis://redis:6379/0"
    opensearch_url: str = "http://opensearch:9200"
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "dtmo"
    minio_secret_key: SecretStr = SecretStr("")
    minio_secure: bool = False
    api_key: SecretStr = SecretStr("")
    auth_header_name: str = "x-dtmo-api-key"
    token_signing_secret: SecretStr = SecretStr("")
    jwt_issuer: str = "https://identity.dtmo.local"
    jwt_audience: str = "dtmo-api"
    connector_poll_seconds: int = Field(default=3600, ge=60)
    connector_timeout_seconds: int = Field(default=30, ge=1, le=300)
    connector_max_attempts: int = Field(default=4, ge=1, le=10)
    publish_requires_human_approval: bool = True
    feature_live_connectors: bool = False
    feature_ai_analyst: bool = False

    @property
    def production(self) -> bool:
        return self.environment == "production"

    @model_validator(mode="after")
    def validate_production_security(self) -> Self:
        if not self.production:
            return self
        if not self.publish_requires_human_approval:
            raise ValueError("production requires human publication approval")
        if not self.minio_secure:
            raise ValueError("production requires TLS for object storage")
        if not self.minio_secret_key.get_secret_value():
            raise ValueError("production requires an object-storage secret")
        if len(self.token_signing_secret.get_secret_value()) < 32:
            raise ValueError("production token signing secret must be at least 32 characters")
        if not self.jwt_issuer.startswith("https://"):
            raise ValueError("production token issuer must use HTTPS")
        if not self.jwt_audience.strip():
            raise ValueError("production token audience is required")
        if not self.database_url.startswith("postgresql+psycopg://"):
            raise ValueError("production requires PostgreSQL with the psycopg driver")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
