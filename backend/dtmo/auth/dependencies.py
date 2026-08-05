from __future__ import annotations

import hmac
from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, status

from dtmo.config import Settings, get_settings

from .policy import Permission, Principal, Role, require


def resolve_principal(
    x_dtmo_subject: str = Header(default="anonymous"),
    x_dtmo_roles: str = Header(default="executive"),
    x_dtmo_api_key: str = Header(default=""),
    settings: Settings = Depends(get_settings),
) -> Principal:
    expected = settings.api_key.get_secret_value()
    if expected and not hmac.compare_digest(x_dtmo_api_key, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid API key")
    if settings.production and not expected:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="authentication unavailable")

    roles: set[Role] = set()
    for value in x_dtmo_roles.split(","):
        token = value.strip().lower()
        if not token:
            continue
        try:
            roles.add(Role(token))
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"unknown role: {token}",
            ) from exc
    if not roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="at least one role is required")
    return Principal(subject=x_dtmo_subject, roles=frozenset(roles))


def require_permission(permission: Permission) -> Callable[[Principal], Principal]:
    def dependency(principal: Principal = Depends(resolve_principal)) -> Principal:
        try:
            require(principal, permission)
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
        return principal

    return dependency
