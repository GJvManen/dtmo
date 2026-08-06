from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException
from pydantic import SecretStr

from dtmo.auth.dependencies import resolve_principal
from dtmo.auth.policy import Role
from dtmo.auth.tokens import PrincipalType, TokenValidationError, decode_principal_token
from dtmo.config import Settings

SECRET = "t" * 32
ISSUER = "https://identity.example.test"
AUDIENCE = "dtmo-api"
JTI = "jwt-123"


def _token(**overrides: object) -> str:
    now = datetime.now(UTC)
    claims: dict[str, object] = {
        "sub": "analyst@example.test",
        "roles": ["analyst"],
        "principal_type": "human",
        "jti": JTI,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "nbf": now - timedelta(seconds=1),
        "exp": now + timedelta(minutes=5),
    }
    claims.update(overrides)
    return jwt.encode(claims, SECRET, algorithm="HS256")


def test_valid_token_establishes_trusted_human_principal() -> None:
    authenticated = decode_principal_token(_token(), secret=SECRET, issuer=ISSUER, audience=AUDIENCE)
    assert authenticated.principal.subject == "analyst@example.test"
    assert authenticated.principal.roles == frozenset({Role.ANALYST})
    assert authenticated.principal_type is PrincipalType.HUMAN
    assert authenticated.jti == JTI


@pytest.mark.parametrize(
    ("overrides", "issuer", "audience"),
    [
        ({"exp": datetime.now(UTC) - timedelta(minutes=1)}, ISSUER, AUDIENCE),
        ({"iss": "https://wrong.example.test"}, ISSUER, AUDIENCE),
        ({"aud": "wrong-api"}, ISSUER, AUDIENCE),
        ({"nbf": datetime.now(UTC) + timedelta(minutes=1)}, ISSUER, AUDIENCE),
    ],
)
def test_invalid_temporal_or_trust_claims_are_rejected(
    overrides: dict[str, object], issuer: str, audience: str
) -> None:
    with pytest.raises(TokenValidationError, match="invalid bearer token"):
        decode_principal_token(_token(**overrides), secret=SECRET, issuer=issuer, audience=audience)


def test_machine_principal_cannot_claim_human_role() -> None:
    with pytest.raises(TokenValidationError, match="machine principals"):
        decode_principal_token(
            _token(principal_type="connector", roles=["analyst"]),
            secret=SECRET,
            issuer=ISSUER,
            audience=AUDIENCE,
        )


def test_human_principal_cannot_claim_service_account_role() -> None:
    with pytest.raises(TokenValidationError, match="human principals"):
        decode_principal_token(
            _token(roles=["service_account"]), secret=SECRET, issuer=ISSUER, audience=AUDIENCE
        )


def _production_settings() -> Settings:
    return Settings(
        environment="production",
        minio_secure=True,
        minio_secret_key=SecretStr("object-secret"),
        token_signing_secret=SecretStr(SECRET),
        jwt_issuer=ISSUER,
        jwt_audience=AUDIENCE,
    )


def test_production_rejects_untrusted_identity_headers() -> None:
    with pytest.raises(HTTPException) as exc_info:
        resolve_principal(
            settings=_production_settings(),
            authorization="",
            x_dtmo_subject="forged@example.test",
            x_dtmo_roles="admin",
            x_dtmo_api_key="",
        )
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "bearer token required"


def test_production_resolves_roles_only_from_signed_token() -> None:
    principal = resolve_principal(
        settings=_production_settings(),
        authorization=f"Bearer {_token()}",
        x_dtmo_subject="forged@example.test",
        x_dtmo_roles="admin",
        x_dtmo_api_key="",
    )
    assert principal.subject == "analyst@example.test"
    assert principal.roles == frozenset({Role.ANALYST})
