from __future__ import annotations

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from dtmo.auth.dependencies import resolve_principal
from dtmo.auth.policy import Role
from dtmo.config import Settings
from dtmo.main import app


def test_principal_resolution_accepts_valid_api_key_and_roles() -> None:
    settings = Settings(environment="test", api_key="a" * 32)
    principal = resolve_principal(
        x_dtmo_subject="analyst@example.org",
        x_dtmo_roles="soc,cert",
        x_dtmo_api_key="a" * 32,
        settings=settings,
    )
    assert principal.subject == "analyst@example.org"
    assert principal.roles == frozenset({Role.SOC, Role.CERT})


def test_principal_resolution_rejects_invalid_api_key() -> None:
    settings = Settings(environment="test", api_key="a" * 32)
    with pytest.raises(HTTPException) as exc:
        resolve_principal(
            x_dtmo_subject="analyst",
            x_dtmo_roles="soc",
            x_dtmo_api_key="wrong",
            settings=settings,
        )
    assert exc.value.status_code == 401


def test_principal_resolution_rejects_unknown_role() -> None:
    settings = Settings(environment="test")
    with pytest.raises(HTTPException) as exc:
        resolve_principal(
            x_dtmo_subject="analyst",
            x_dtmo_roles="superuser",
            x_dtmo_api_key="",
            settings=settings,
        )
    assert exc.value.status_code == 400


def test_openapi_exposes_secured_intelligence_routes() -> None:
    with TestClient(app) as client:
        schema = client.get("/openapi.json").json()
    assert "/api/v1/intelligence" in schema["paths"]
    assert "/api/v1/intelligence/search" in schema["paths"]
