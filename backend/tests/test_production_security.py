from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from dtmo.config import Settings

JWKS_JSON = json.dumps(
    {
        "keys": [
            {
                "kty": "RSA",
                "kid": "active-key",
                "use": "sig",
                "alg": "RS256",
                "n": "sXchvR7fYQ",
                "e": "AQAB",
            }
        ]
    }
)


def test_production_rejects_insecure_object_storage() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            minio_secure=False,
            minio_secret_key="secret-value",
            jwt_jwks_json=JWKS_JSON,
        )


def test_production_rejects_missing_object_storage_secret() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            minio_secure=True,
            minio_secret_key="",
            jwt_jwks_json=JWKS_JSON,
        )


def test_production_rejects_missing_jwks() -> None:
    with pytest.raises(ValidationError, match="JWKS"):
        Settings(
            environment="production",
            minio_secure=True,
            minio_secret_key="secret-value",
        )


def test_production_rejects_shared_secret_token_validation() -> None:
    with pytest.raises(ValidationError, match="forbids shared-secret"):
        Settings(
            environment="production",
            minio_secure=True,
            minio_secret_key="secret-value",
            token_signing_secret="t" * 32,
            jwt_jwks_json=JWKS_JSON,
        )


def test_production_accepts_secure_human_gated_configuration() -> None:
    settings = Settings(
        environment="production",
        minio_secure=True,
        minio_secret_key="secret-value",
        jwt_jwks_json=JWKS_JSON,
        publish_requires_human_approval=True,
        database_url="postgresql+psycopg://dtmo@postgres:5432/dtmo",
    )
    assert settings.production
