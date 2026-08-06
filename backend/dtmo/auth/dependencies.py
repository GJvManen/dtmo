from __future__ import annotations

import hmac
from collections.abc import Awaitable, Callable
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status

from dtmo.config import Settings, get_settings
from dtmo.persistence.session import Database

from .authorization_audit import record_authorization_denial
from .policy import Permission, Principal, Role, require
from .token_state import TokenStateError, TokenStateStore
from .tokens import TokenValidationError, decode_principal_token

_audit_database = Database()


def _legacy_development_principal(
    *,
    settings: Settings,
    subject: str,
    roles_header: str,
    api_key: str,
) -> Principal:
    if settings.production:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="bearer token required")
    expected = settings.api_key.get_secret_value()
    if expected and not hmac.compare_digest(api_key, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid API key")

    roles: set[Role] = set()
    for value in roles_header.split(","):
        token = value.strip().lower()
        if not token:
            continue
        try:
            roles.add(Role(token))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"unknown role: {token}") from exc
    try:
        return Principal(subject=subject, roles=frozenset(roles))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


def resolve_principal(
    settings: Annotated[Settings, Depends(get_settings)],
    authorization: Annotated[str, Header()] = "",
    x_dtmo_subject: Annotated[str, Header()] = "anonymous",
    x_dtmo_roles: Annotated[str, Header()] = "executive",
    x_dtmo_api_key: Annotated[str, Header()] = "",
) -> Principal:
    scheme, _, credential = authorization.partition(" ")
    if authorization:
        if scheme.lower() != "bearer" or not credential.strip():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid authorization header")
        try:
            authenticated = decode_principal_token(
                credential.strip(),
                secret=settings.token_signing_secret.get_secret_value(),
                jwks_json=settings.jwt_jwks_json.get_secret_value(),
                issuer=settings.jwt_issuer,
                audience=settings.jwt_audience,
            )
            if settings.production:
                TokenStateStore.from_url(settings.redis_url).assert_active(authenticated)
        except (TokenValidationError, TokenStateError) as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
        return authenticated.principal

    return _legacy_development_principal(
        settings=settings,
        subject=x_dtmo_subject,
        roles_header=x_dtmo_roles,
        api_key=x_dtmo_api_key,
    )


async def _persist_authorization_denial(
    *,
    principal: Principal,
    permission: Permission,
    resource: str,
    request_id: str,
) -> None:
    async for session in _audit_database.session():
        await record_authorization_denial(
            session,
            principal=principal,
            permission=permission,
            resource=resource,
            request_id=request_id,
        )
        return


def require_permission(permission: Permission) -> Callable[..., Awaitable[Principal]]:
    async def dependency(
        request: Request,
        principal: Annotated[Principal, Depends(resolve_principal)],
        request_id: Annotated[str, Header(alias="X-Request-ID")] = "",
    ) -> Principal:
        try:
            require(principal, permission)
        except PermissionError as exc:
            try:
                await _persist_authorization_denial(
                    principal=principal,
                    permission=permission,
                    resource=request.url.path,
                    request_id=request_id,
                )
            except Exception as audit_exc:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="authorization denied; audit backend unavailable",
                ) from audit_exc
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
        return principal

    return dependency
