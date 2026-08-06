from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import HTTPException
from jwt.algorithms import RSAAlgorithm
from pydantic import SecretStr

from dtmo.auth.dependencies import resolve_principal
from dtmo.auth.policy import Role
from dtmo.auth.token_state import TokenStateStore
from dtmo.auth.tokens import AuthenticatedPrincipal, PrincipalType, TokenValidationError, decode_principal_token
from dtmo.config import Settings

ISSUER = "https://identity.example.test"
AUDIENCE = "dtmo-api"
JTI = "jwt-123"
ACTIVE_KID = "key-2026-08"
PREVIOUS_KID = "key-2026-07"
ACTIVE_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PREVIOUS_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)


def _jwk(private_key: rsa.RSAPrivateKey, kid: str) -> dict[str, object]:
    value = RSAAlgorithm.to_jwk(private_key.public_key(), as_dict=True)
    value.update({"kid": kid, "alg": "RS256", "use": "sig"})
    return value


JWKS_JSON = json.dumps(
    {"keys": [_jwk(PREVIOUS_PRIVATE_KEY, PREVIOUS_KID), _jwk(ACTIVE_PRIVATE_KEY, ACTIVE_KID)]}
)


def _claims(**overrides: object) -> dict[str, object]:
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
    return claims


def _token(
    *,
    private_key: rsa.RSAPrivateKey = ACTIVE_PRIVATE_KEY,
    kid: str = ACTIVE_KID,
    **overrides: object,
) -> str:
    return jwt.encode(
        _claims(**overrides),
        private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )


def _decode(token: str, *, issuer: str = ISSUER, audience: str = AUDIENCE) -> object:
    return decode_principal_token(
        token,
        jwks_json=JWKS_JSON,
        issuer=issuer,
        audience=audience,
    )


def test_valid_token_establishes_trusted_human_principal() -> None:
    authenticated = decode_principal_token(
        _token(), jwks_json=JWKS_JSON, issuer=ISSUER, audience=AUDIENCE
    )
    assert authenticated.principal.subject == "analyst@example.test"
    assert authenticated.principal.roles == frozenset({Role.ANALYST})
    assert authenticated.principal_type is PrincipalType.HUMAN
    assert authenticated.jti == JTI


def test_jwks_rotation_accepts_active_and_previous_signing_keys() -> None:
    active = decode_principal_token(
        _token(), jwks_json=JWKS_JSON, issuer=ISSUER, audience=AUDIENCE
    )
    previous = decode_principal_token(
        _token(private_key=PREVIOUS_PRIVATE_KEY, kid=PREVIOUS_KID),
        jwks_json=JWKS_JSON,
        issuer=ISSUER,
        audience=AUDIENCE,
    )
    assert active.principal == previous.principal


def test_unknown_kid_is_rejected() -> None:
    with pytest.raises(TokenValidationError, match="exactly one trusted signing key"):
        _decode(_token(kid="unknown-key"))


def test_algorithm_confusion_is_rejected_before_signature_validation() -> None:
    token = jwt.encode(_claims(), "h" * 32, algorithm="HS256", headers={"kid": ACTIVE_KID})
    with pytest.raises(TokenValidationError, match="must use RS256"):
        _decode(token)


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
        _decode(_token(**overrides), issuer=issuer, audience=audience)


def test_machine_principal_cannot_claim_human_role() -> None:
    with pytest.raises(TokenValidationError, match="machine principals"):
        _decode(_token(principal_type="connector", roles=["analyst"]))


def test_human_principal_cannot_claim_service_account_role() -> None:
    with pytest.raises(TokenValidationError, match="human principals"):
        _decode(_token(roles=["service_account"]))


def _production_settings() -> Settings:
    return Settings(
        environment="production",
        minio_secure=True,
        minio_secret_key=SecretStr("object-secret"),
        jwt_jwks_json=SecretStr(JWKS_JSON),
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


def test_production_resolves_roles_only_from_jwks_validated_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ActiveTokenState:
        def assert_active(self, authenticated: AuthenticatedPrincipal) -> None:
            assert authenticated.jti == JTI

    monkeypatch.setattr(
        TokenStateStore,
        "from_url",
        staticmethod(lambda _url: ActiveTokenState()),
    )
    principal = resolve_principal(
        settings=_production_settings(),
        authorization=f"Bearer {_token()}",
        x_dtmo_subject="forged@example.test",
        x_dtmo_roles="admin",
        x_dtmo_api_key="",
    )
    assert principal.subject == "analyst@example.test"
    assert principal.roles == frozenset({Role.ANALYST})
