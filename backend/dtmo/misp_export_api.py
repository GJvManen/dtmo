from __future__ import annotations

from typing import Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.config import Settings, get_settings
from dtmo.governance import (
    MispExportError,
    deliver_misp_event,
    finalize_misp_export,
    mark_misp_export_uncertain,
    prepare_misp_export,
)


router = APIRouter(prefix="/api/v1", tags=["misp-export"])


def _validate_runtime_export_settings(settings: Settings) -> None:
    if not settings.feature_misp_export:
        raise MispExportError("MISP export feature is disabled")
    if not settings.misp_api_base.rstrip("/"):
        raise MispExportError("MISP export requires a configured API base")
    if not settings.misp_api_key.get_secret_value().strip():
        raise MispExportError("MISP export requires a runtime API key")
    if settings.production and not settings.misp_api_base.startswith("https://"):
        raise MispExportError("production MISP export requires HTTPS")


@router.post("/intelligence/{item_id}/misp-export")
async def export_intelligence_to_misp(
    item_id: UUID,
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.SHARE_APPROVE)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
    distribution: int = Query(default=0, ge=0, le=4),
    sharing_group_id: str | None = Query(default=None, max_length=64),
    tlp: str = Query(default="tlp:amber", min_length=3, max_length=32),
) -> dict[str, str | None]:
    """Export one already reviewed and share-approved DTMO item to MISP.

    This endpoint never grants share approval and never publishes the resulting
    MISP event. The destination event is created unpublished; any later MISP
    publication/synchronisation remains a separate governed action.
    """

    try:
        _validate_runtime_export_settings(settings)
        prepared = await session.run_sync(
            lambda sync_session: prepare_misp_export(
                sync_session,
                item_id=item_id,
                principal=principal,
                request_id=request_id,
                distribution=distribution,
                sharing_group_id=sharing_group_id,
                tlp=tlp,
            )
        )
    except MispExportError as exc:
        await session.commit()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    # The replay reservation must be durable before any external side effect.
    # If the process stops after MISP accepts the event but before DTMO can
    # finalize the response, the persisted pending record blocks automatic
    # replay and forces operator inspection instead of risking a duplicate.
    await session.commit()

    try:
        async with httpx.AsyncClient(timeout=settings.connector_timeout_seconds) as client:
            misp_event_id = await deliver_misp_event(prepared, settings=settings, client=client)
    except (httpx.HTTPError, ValueError, MispExportError) as exc:
        await session.run_sync(
            lambda sync_session: mark_misp_export_uncertain(
                sync_session,
                prepared=prepared,
                principal=principal,
                request_id=request_id,
            )
        )
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "MISP delivery result is uncertain; automatic replay is blocked pending operator inspection"
            ),
        ) from exc

    result = await session.run_sync(
        lambda sync_session: finalize_misp_export(
            sync_session,
            prepared=prepared,
            principal=principal,
            request_id=request_id,
            misp_event_id=misp_event_id,
        )
    )
    return {
        "id": str(result.item_id),
        "replay_key": result.replay_key,
        "event_uuid": result.event_uuid,
        "misp_event_id": result.misp_event_id,
        "audit_event_id": str(result.audit_event_id),
    }
