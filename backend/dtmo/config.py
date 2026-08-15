from __future__ import annotations

import json
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
    jwt_jwks_json: SecretStr = SecretStr("")
    jwt_issuer: str = "https://identity.dtmo.local"
    jwt_audience: str = "dtmo-api"
    privacy_pseudonymization_secret: SecretStr = SecretStr("")
    audit_projection_retention_days: int = Field(default=365, ge=30, le=3650)
    identity_projection_retention_days: int = Field(default=90, ge=1, le=730)
    connector_poll_seconds: int = Field(default=3600, ge=60)
    connector_timeout_seconds: int = Field(default=30, ge=1, le=300)
    connector_max_attempts: int = Field(default=4, ge=1, le=10)
    opencve_api_base: str = "https://app.opencve.io/api/v2"
    opencve_api_token: SecretStr = SecretStr("")
    opencve_page_size: int = Field(default=20, ge=1, le=100)
    opencve_max_pages: int = Field(default=1, ge=1, le=20)
    vulnerability_lookup_api_base: str = "https://vulnerability.circl.lu/api"
    vulnerability_lookup_api_token: SecretStr = SecretStr("")
    vulnerability_lookup_page_size: int = Field(default=50, ge=1, le=1000)
    vulnerability_lookup_since: str = ""
    vulnerability_lookup_user_agent: str = "DTMO vulnerability-intelligence connector (contact: repository owner)"
    misp_api_base: str = ""
    misp_api_key: SecretStr = SecretStr("")
    misp_event_limit: int = Field(default=50, ge=1, le=500)
    ail_api_base: str = ""
    ail_api_key: SecretStr = SecretStr("")
    ail_object_global_ids: str = ""
    ail_object_limit: int = Field(default=50, ge=1, le=500)
    taranis_api_base: str = ""
    taranis_api_token: SecretStr = SecretStr("")
    taranis_page_size: int = Field(default=100, ge=1, le=400)
    publish_requires_human_approval: bool = True
    feature_live_connectors: bool = False
    feature_opencve_connector: bool = False
    feature_vulnerability_lookup_connector: bool = False
    feature_misp_connector: bool = False
    feature_misp_export: bool = False
    feature_ail_connector: bool = False
    feature_taranis_connector: bool = False
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
        if self.token_signing_secret.get_secret_value():
            raise ValueError("production forbids shared-secret token validation")
        jwks_json = self.jwt_jwks_json.get_secret_value()
        try:
            jwks = json.loads(jwks_json)
        except json.JSONDecodeError as exc:
            raise ValueError("production requires a valid JWKS document") from exc
        if not isinstance(jwks, dict) or not isinstance(jwks.get("keys"), list) or not jwks["keys"]:
            raise ValueError("production requires at least one JWKS signing key")
        if not self.jwt_issuer.startswith("https://"):
            raise ValueError("production token issuer must use HTTPS")
        if not self.jwt_audience.strip():
            raise ValueError("production token audience is required")
        if not self.database_url.startswith("postgresql+psycopg://"):
            raise ValueError("production requires PostgreSQL with the psycopg driver")
        if len(self.privacy_pseudonymization_secret.get_secret_value()) < 32:
            raise ValueError("production privacy pseudonymization secret must be at least 32 characters")
        if self.identity_projection_retention_days > self.audit_projection_retention_days:
            raise ValueError("identity projection retention cannot exceed audit projection retention")
        if self.feature_misp_connector or self.feature_misp_export:
            if not self.misp_api_base.startswith("https://"):
                raise ValueError("production MISP integration requires an HTTPS API base")
            if not self.misp_api_key.get_secret_value().strip():
                raise ValueError("production MISP integration requires a runtime API key")
        if self.feature_ail_connector:
            if not self.ail_api_base.startswith("https://"):
                raise ValueError("production AIL integration requires an HTTPS API base")
            if not self.ail_api_key.get_secret_value().strip():
                raise ValueError("production AIL integration requires a runtime API key")
            if not self.ail_object_global_ids.strip():
                raise ValueError("production AIL integration requires explicit object global ids")
        if self.feature_taranis_connector:
            if not self.taranis_api_base.startswith("https://"):
                raise ValueError("production Taranis integration requires an HTTPS API base")
            if not self.taranis_api_token.get_secret_value().strip():
                raise ValueError("production Taranis integration requires a runtime API token")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
