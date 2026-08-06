from __future__ import annotations

import hmac
from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from dtmo.config import Settings, get_settings

from .policy import Permission, Principal, Role, require
from .tokens import TokenValidationError, decode_principal_token


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
    authorization: str = Header(default=""),
    x_dtmo_subject: str = Header(default="anonymous"),
    x_dtmo_roles: str = Header(default="executive"),
    x_dtmo_api_key: str = Header(default=""),
) -> Principal:
    scheme, _, credential = authorization.partition(" ")
    if authorization:
        if scheme.lower() != "bearer" or not credential.strip():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid authorization header")
        try:
            authenticated = decode_principal_token(
                credential.strip(),
                secret=settings.token_signing_secret.get_secret_value(),
                issuer=settings.jwt_issuer,
                audience=settings.jwt_audience,
            )
        except TokenValidationError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
        return authenticated.principal

    return _legacy_development_principal(
        settings=settings,
        subject=x_dtmo_subject,
        roles_header=x_dtmo_roles,
        api_key=x_dtmo_api_key,
    )


def require_permission(permission: Permission) -> Callable[[Principal], Principal]:
    def dependency(principal: Annotated[Principal, Depends(resolve_principal)]) -> Principal:
        try:
            require(principal, permission)
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
        return principal

    return dependency
