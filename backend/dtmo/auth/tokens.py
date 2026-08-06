from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

import jwt
from jwt.types import Options

from .policy import Principal, Role


class PrincipalType(StrEnum):
    HUMAN = "human"
    SERVICE_ACCOUNT = "service_account"
    CONNECTOR = "connector"
    SCHEDULER = "scheduler"


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    principal: Principal
    principal_type: PrincipalType
    jti: str
    issuer: str
    authenticated_at: datetime
    expires_at: datetime
    one_time: bool = False


class TokenValidationError(ValueError):
    """Raised when a bearer token cannot establish a trusted principal."""


def _select_jwks_key(token: str, jwks_json: str) -> jwt.PyJWK:
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        algorithm = header.get("alg")
        payload = json.loads(jwks_json)
    except (jwt.PyJWTError, json.JSONDecodeError, TypeError) as exc:
        raise TokenValidationError("invalid bearer token or JWKS document") from exc

    if algorithm != "RS256":
        raise TokenValidationError("bearer token must use RS256")
    if not isinstance(kid, str) or not kid.strip():
        raise TokenValidationError("bearer token requires a key identifier")
    if not isinstance(payload, dict) or not isinstance(payload.get("keys"), list):
        raise TokenValidationError("JWKS document must contain a keys list")

    matching_keys: list[dict[str, Any]] = []
    for value in payload["keys"]:
        if not isinstance(value, dict):
            continue
        if value.get("kid") != kid:
            continue
        if value.get("kty") != "RSA" or value.get("alg") not in (None, "RS256"):
            continue
        if value.get("use") not in (None, "sig"):
            continue
        matching_keys.append(value)

    if len(matching_keys) != 1:
        raise TokenValidationError("JWKS must contain exactly one trusted signing key for kid")

    try:
        return jwt.PyJWK.from_dict(matching_keys[0], algorithm="RS256")
    except (jwt.PyJWTError, ValueError, TypeError) as exc:
        raise TokenValidationError("JWKS signing key is invalid") from exc


def decode_principal_token(
    token: str,
    *,
    issuer: str,
    audience: str,
    jwks_json: str = "",
    secret: str = "",
    now: datetime | None = None,
) -> AuthenticatedPrincipal:
    if not token:
        raise TokenValidationError("token authentication is not configured")
    if bool(jwks_json) == bool(secret):
        raise TokenValidationError("configure exactly one token trust source")

    options: Options = {
        "require": ["sub", "roles", "principal_type", "jti", "iss", "aud", "iat", "nbf", "exp"],
    }
    algorithm = "RS256" if jwks_json else "HS256"
    key = _select_jwks_key(token, jwks_json) if jwks_json else secret
    try:
        claims = jwt.decode(
            token,
            key,
            algorithms=[algorithm],
            issuer=issuer,
            audience=audience,
            options=options,
            leeway=5,
        )
    except jwt.PyJWTError as exc:
        raise TokenValidationError("invalid bearer token") from exc

    roles_claim = claims.get("roles")
    if not isinstance(roles_claim, list) or not roles_claim:
        raise TokenValidationError("token roles must be a non-empty list")
    try:
        roles = frozenset(Role(str(value).strip().lower()) for value in roles_claim)
        principal_type = PrincipalType(str(claims["principal_type"]).strip().lower())
    except (TypeError, ValueError) as exc:
        raise TokenValidationError("token contains an unknown role or principal type") from exc

    if principal_type is not PrincipalType.HUMAN and roles != frozenset({Role.SERVICE_ACCOUNT}):
        raise TokenValidationError("machine principals must use only the service_account role")
    if principal_type is PrincipalType.HUMAN and Role.SERVICE_ACCOUNT in roles:
        raise TokenValidationError("human principals cannot use the service_account role")

    subject = str(claims["sub"]).strip()
    jti = str(claims["jti"]).strip()
    one_time_claim = claims.get("one_time", False)
    if not subject or not jti:
        raise TokenValidationError("token subject and identifier are required")
    if not isinstance(one_time_claim, bool):
        raise TokenValidationError("token one_time claim must be boolean")

    return AuthenticatedPrincipal(
        principal=Principal(subject=subject, roles=roles),
        principal_type=principal_type,
        jti=jti,
        issuer=str(claims["iss"]),
        authenticated_at=now or datetime.now(UTC),
        expires_at=datetime.fromtimestamp(int(claims["exp"]), tz=UTC),
        one_time=one_time_claim,
    )
