from __future__ import annotations

import re
from typing import Any

from dtmo.connectors.base import ConnectorRecord

MAX_MSRC_UPDATES_PER_RUN = 12
_UPDATE_ID = re.compile(r"^\d{4}-[a-z]{3}$", re.IGNORECASE)


class MSRCAdapterError(ValueError):
    pass


def parse_msrc_update_ids(payload: Any) -> list[str]:
    """Return a bounded list of valid MSRC CVRF document IDs from /updates."""
    if not isinstance(payload, dict) or not isinstance(payload.get("value"), list):
        raise MSRCAdapterError("MSRC updates response must expose a value list")
    candidates: list[tuple[str, str]] = []
    for item in payload["value"]:
        if not isinstance(item, dict):
            continue
        update_id = str(item.get("ID") or item.get("id") or "").strip()
        if not _UPDATE_ID.fullmatch(update_id):
            continue
        released = str(item.get("CurrentReleaseDate") or item.get("currentReleaseDate") or "")
        candidates.append((released, update_id.lower()))
    if not candidates:
        raise MSRCAdapterError("MSRC updates response contained no valid CVRF document IDs")
    candidates.sort(reverse=True)
    seen: set[str] = set()
    result: list[str] = []
    for _released, update_id in candidates:
        if update_id in seen:
            continue
        seen.add(update_id)
        result.append(update_id)
        if len(result) >= MAX_MSRC_UPDATES_PER_RUN:
            break
    return result


def _title(payload: dict[str, Any], update_id: str) -> str:
    document_title = payload.get("DocumentTitle")
    if isinstance(document_title, dict):
        value = document_title.get("Value") or document_title.get("value")
        if isinstance(value, str) and value.strip():
            return value.strip()
    if isinstance(document_title, str) and document_title.strip():
        return document_title.strip()
    return f"Microsoft Security Update {update_id}"


def _summary(payload: dict[str, Any]) -> str:
    notes = payload.get("DocumentNotes")
    if isinstance(notes, list):
        for note in notes:
            if isinstance(note, dict):
                value = note.get("Value") or note.get("value")
                if isinstance(value, str) and value.strip():
                    return value.strip()
    return "Microsoft Security Response Center CVRF security update."


def parse_msrc_cvrf_document(
    payload: Any,
    *,
    update_id: str,
    reliability: str,
    document_url: str,
) -> ConnectorRecord:
    if not _UPDATE_ID.fullmatch(update_id):
        raise MSRCAdapterError("invalid MSRC CVRF document ID")
    if not isinstance(payload, dict):
        raise MSRCAdapterError("MSRC CVRF document must be a JSON object")
    if not payload.get("Vulnerability") and not payload.get("ProductTree"):
        raise MSRCAdapterError("MSRC CVRF document has no vulnerability or product data")
    tracking = payload.get("DocumentTracking")
    published_at: str | None = None
    if isinstance(tracking, dict):
        value = tracking.get("CurrentReleaseDate") or tracking.get("InitialReleaseDate")
        if value:
            published_at = str(value)
    return ConnectorRecord(
        external_id=f"MSRC-{update_id.lower()}",
        object_type="security-advisory",
        title=_title(payload, update_id),
        url=document_url,
        summary=_summary(payload),
        published_at=published_at,
        source_reliability=reliability,
        confidence=95,
        raw=payload,
    )
