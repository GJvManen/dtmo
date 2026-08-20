from __future__ import annotations

from typing import Annotated, Any
from uuid import NAMESPACE_URL, UUID, uuid5

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.config import Settings, get_settings
from dtmo.persistence.models import IntelligenceItem

router = APIRouter(prefix="/sharing", tags=["misp-sharing-workspace"])


def _safe_restrictions(item: IntelligenceItem) -> dict[str, Any] | None:
    value = item.metadata_json.get("misp_restrictions")
    if not isinstance(value, dict):
        return None
    return {
        "restriction_authoritative": bool(value.get("restriction_authoritative")),
        "distribution": value.get("distribution"),
        "sharing_group_id": value.get("sharing_group_id"),
        "tlp_tags": [str(tag) for tag in value.get("tlp_tags", []) if isinstance(tag, str)],
    }


def _safe_exports(item: IntelligenceItem) -> list[dict[str, Any]]:
    value = item.metadata_json.get("misp_exports")
    if not isinstance(value, list):
        return []
    exports: list[dict[str, Any]] = []
    for record in value:
        if not isinstance(record, dict):
            continue
        exports.append(
            {
                "status": str(record.get("status", "unknown")),
                "event_uuid": str(record.get("event_uuid", "")),
                "misp_event_id": str(record.get("misp_event_id", "")) or None,
                "distribution": str(record.get("distribution", "")) or None,
                "sharing_group_id": str(record.get("sharing_group_id", "")) or None,
                "tlp": str(record.get("tlp", "")) or None,
                "requested_by": str(record.get("requested_by", "")) or None,
            }
        )
    return exports


def _current_event_uuid(item: IntelligenceItem) -> str:
    return str(uuid5(NAMESPACE_URL, f"dtmo:misp-export:{item.id}:{item.content_hash}"))


@router.get("/items/{item_id}")
async def misp_sharing_item_state(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, object]:
    item = await session.get(IntelligenceItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="intelligence item not found")

    reviewed_by = str(item.metadata_json.get("reviewed_by", "")).strip() or None
    share_approved_by = str(item.metadata_json.get("share_approved_by", "")).strip() or None
    restrictions = _safe_restrictions(item)
    exports = _safe_exports(item)
    current_event_uuid = _current_event_uuid(item)
    current_export = next(
        (
            record
            for record in exports
            if record.get("event_uuid") == current_event_uuid
            and record.get("status") in {"pending", "success", "uncertain"}
        ),
        None,
    )

    blockers: list[str] = []
    if item.review_status != "reviewed":
        blockers.append("independent human review required")
    if item.review_status == "reviewed" and reviewed_by is None:
        blockers.append("review attribution missing")
    if not item.share_approved:
        blockers.append("separate human share approval required")
    if item.share_approved and share_approved_by is None:
        blockers.append("share approval attribution missing")
    if item.source_id == "misp" and not (restrictions and restrictions.get("restriction_authoritative")):
        blockers.append("authoritative MISP source restrictions required before re-export")
    if current_export is not None:
        blockers.append(f"current canonical revision already has {current_export['status']} export evidence")

    configured = bool(
        settings.misp_api_base.rstrip("/")
        and settings.misp_api_key.get_secret_value().strip()
    )

    return {
        "item_id": str(item.id),
        "title": item.title,
        "source_id": item.source_id,
        "canonical_url": item.canonical_url,
        "review_status": item.review_status,
        "reviewed_by": reviewed_by,
        "share_approved": item.share_approved,
        "share_approved_by": share_approved_by,
        "misp_restrictions": restrictions,
        "misp_exports": exports,
        "current_event_uuid": current_event_uuid,
        "export_eligible": not blockers,
        "export_blockers": blockers,
        "principal_actions": {
            "can_review": principal.can(Permission.REVIEW_INTELLIGENCE) and not principal.is_service_account,
            "can_approve_share": principal.can(Permission.SHARE_APPROVE) and not principal.is_service_account,
        },
        "misp_export_enabled": bool(settings.feature_misp_export),
        "misp_export_configured": configured,
        "runtime_health_claim": False,
        "publication_authority": False,
        "synchronization_authority": False,
        "evidence_boundary": (
            "Sharing state is derived from canonical DTMO persistence and configuration only. "
            "Configuration does not prove live MISP health. Review and share approval remain separate human decisions. "
            "Export creates an unpublished MISP event and grants no MISP publication or synchronization authority."
        ),
    }
