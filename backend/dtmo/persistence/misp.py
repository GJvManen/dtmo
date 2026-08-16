from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from dtmo.persistence.models import Base, IntelligenceItem


def utc_now() -> datetime:
    return datetime.now(UTC)


class MispSynchronizationState(Base):
    """Durable inbound MISP identity and authority envelope for one canonical item."""

    __tablename__ = "misp_synchronization_state"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("intelligence_items.id", ondelete="CASCADE"), nullable=False, unique=True)
    event_uuid: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    event_timestamp: Mapped[str | None] = mapped_column(String(64), nullable=True)
    distribution: Mapped[str] = mapped_column(String(1), nullable=False)
    sharing_group_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    tlp_tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    authority_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    snapshot_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    external_share_authorized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("event_uuid", "snapshot_hash", name="uq_misp_sync_event_snapshot"),
        CheckConstraint("distribution IN ('0','1','2','3','4','5')", name="ck_misp_sync_distribution"),
        CheckConstraint(
            "(distribution = '4' AND sharing_group_id IS NOT NULL) OR distribution <> '4'",
            name="ck_misp_sync_sharing_group_required",
        ),
        CheckConstraint("external_share_authorized = false", name="ck_misp_sync_no_share_authority"),
    )


def authority_snapshot(projection: dict[str, Any]) -> dict[str, Any]:
    event_uuid = projection.get("event_uuid")
    distribution = projection.get("distribution")
    distribution_value = distribution.get("value") if isinstance(distribution, dict) else distribution
    sharing_group_id = projection.get("sharing_group_id")
    tlp_tags = projection.get("tlp_tags")
    if not isinstance(event_uuid, str) or not event_uuid.strip():
        raise ValueError("MISP synchronization requires event UUID")
    if str(distribution_value) not in {"0", "1", "2", "3", "4", "5"}:
        raise ValueError("MISP synchronization requires known distribution")
    if str(distribution_value) == "4" and not str(sharing_group_id or "").strip():
        raise ValueError("MISP sharing-group distribution requires sharing_group_id")
    if not isinstance(tlp_tags, list):
        raise ValueError("MISP synchronization requires explicit TLP tag list")
    if projection.get("restriction_authoritative") is not True:
        raise ValueError("MISP restrictions are not authoritative")
    if projection.get("read_only_import") is not True:
        raise ValueError("MISP synchronization accepts read-only imports only")
    if projection.get("external_share_authorized") is not False:
        raise ValueError("MISP import cannot grant external share authority")
    return {
        "event_uuid": event_uuid.strip(),
        "event_timestamp": projection.get("timestamp"),
        "distribution": str(distribution_value),
        "sharing_group_id": str(sharing_group_id).strip() if sharing_group_id not in {None, ""} else None,
        "tlp_tags": sorted(str(tag).strip().lower() for tag in tlp_tags),
        "restriction_authoritative": True,
        "external_share_authorized": False,
    }


def snapshot_hash(snapshot: dict[str, Any]) -> str:
    encoded = json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def reconcile_misp_state(
    session: Session,
    *,
    item_id: UUID,
    projection: dict[str, Any],
) -> MispSynchronizationState:
    item = session.get(IntelligenceItem, item_id)
    if item is None:
        raise KeyError(item_id)
    snapshot = authority_snapshot(projection)
    digest = snapshot_hash(snapshot)
    event_uuid = str(snapshot["event_uuid"])
    existing_by_item = session.scalar(
        select(MispSynchronizationState).where(MispSynchronizationState.item_id == item_id).with_for_update()
    )
    existing_by_event = session.scalar(
        select(MispSynchronizationState).where(MispSynchronizationState.event_uuid == event_uuid).with_for_update()
    )
    if existing_by_event is not None and existing_by_event.item_id != item_id:
        raise ValueError("MISP event UUID is already mapped to another DTMO item")
    if existing_by_item is not None and existing_by_item.event_uuid != event_uuid:
        raise ValueError("DTMO item MISP event identity changed")

    state = existing_by_item or existing_by_event
    if state is None:
        state = MispSynchronizationState(
            item_id=item_id,
            event_uuid=event_uuid,
            event_timestamp=snapshot.get("event_timestamp"),
            distribution=str(snapshot["distribution"]),
            sharing_group_id=snapshot.get("sharing_group_id"),
            tlp_tags=list(snapshot["tlp_tags"]),
            authority_snapshot=snapshot,
            snapshot_hash=digest,
            external_share_authorized=False,
        )
        session.add(state)
    elif state.snapshot_hash != digest:
        state.event_timestamp = snapshot.get("event_timestamp")
        state.distribution = str(snapshot["distribution"])
        state.sharing_group_id = snapshot.get("sharing_group_id")
        state.tlp_tags = list(snapshot["tlp_tags"])
        state.authority_snapshot = snapshot
        state.snapshot_hash = digest

    state.last_seen_at = utc_now()
    item.metadata_json = {
        **item.metadata_json,
        "misp_restrictions": snapshot,
    }
    session.flush()
    return state
