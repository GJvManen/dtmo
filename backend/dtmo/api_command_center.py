from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.command_center import build_command_center_snapshot
from dtmo.config import Settings, get_settings

router = APIRouter(prefix="/api/v1/command-center", tags=["command-center"])


@router.get("")
async def command_center_snapshot(
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.READ_INTELLIGENCE)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, Any]:
    """Return the canonical, read-only Command Center projection.

    This endpoint grants no review, share, case, connector or administration
    authority. UI visibility remains subordinate to the server-side permissions
    enforced by the corresponding mutation endpoints.
    """

    del principal
    return await build_command_center_snapshot(session, settings)
