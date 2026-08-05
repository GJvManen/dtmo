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
        )


def test_production_rejects_missing_object_storage_secret() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            minio_secure=True,
            minio_secret_key="",
        )


def test_production_accepts_secure_human_gated_configuration() -> None:
    settings = Settings(
        environment="production",
        minio_secure=True,
        minio_secret_key="secret-value",
        publish_requires_human_approval=True,
        database_url="postgresql+psycopg://dtmo@postgres:5432/dtmo",
    )
    assert settings.production
