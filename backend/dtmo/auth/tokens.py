from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

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


class TokenValidationError(ValueError):
    """Raised when a bearer token cannot establish a trusted principal."""


def decode_principal_token(
    token: str,
    *,
    secret: str,
    issuer: str,
    audience: str,
    now: datetime | None = None,
) -> AuthenticatedPrincipal:
    if not token or not secret:
        raise TokenValidationError("token authentication is not configured")

    options: Options = {
        "require": ["sub", "roles", "principal_type", "jti", "iss", "aud", "iat", "nbf", "exp"],
    }
    try:
        claims = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
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
    if not subject or not jti:
        raise TokenValidationError("token subject and identifier are required")

    return AuthenticatedPrincipal(
        principal=Principal(subject=subject, roles=roles),
        principal_type=principal_type,
        jti=jti,
        issuer=str(claims["iss"]),
        authenticated_at=now or datetime.now(UTC),
    )
