from __future__ import annotations

import pytest
from pydantic import ValidationError

from dtmo.config import Settings


def test_production_rejects_insecure_object_storage() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            minio_secure=False,
            minio_secret_key="secret-value",
            api_key="a" * 32,
        )


def test_production_rejects_missing_object_storage_secret() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            minio_secure=True,
            minio_secret_key="",
            api_key="a" * 32,
        )


def test_production_rejects_missing_or_short_api_key() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            minio_secure=True,
            minio_secret_key="secret-value",
            api_key="short",
        )


def test_production_accepts_secure_human_gated_configuration() -> None:
    settings = Settings(
        environment="production",
        minio_secure=True,
        minio_secret_key="secret-value",
        api_key="a" * 32,
        token_signing_secret="t" * 32,
        publish_requires_human_approval=True,
        database_url="postgresql+psycopg://dtmo@postgres:5432/dtmo",
    )
    assert settings.production
