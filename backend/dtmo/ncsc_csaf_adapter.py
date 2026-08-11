from __future__ import annotations

import re
from typing import Any

from dtmo.connectors.base import ConnectorRecord

MAX_CSAF_DOCUMENTS_PER_RUN = 25
_CSAF_PATH = re.compile(r"^(20\d{2})/([a-z0-9-]+\.json)$")


class CSAFAdapterError(RuntimeError):
    pass


def parse_csaf_index(payload: bytes) -> list[str]:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CSAFAdapterError("CSAF index is not valid UTF-8") from exc
    paths: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip().lower()
        if not line:
            continue
        if not _CSAF_PATH.fullmatch(line):
            raise CSAFAdapterError("CSAF index contains an invalid advisory path")
        paths.append(line)
        if len(paths) >= MAX_CSAF_DOCUMENTS_PER_RUN:
            break
    if not paths:
        raise CSAFAdapterError("CSAF index contains no advisory documents")
    return paths


def _summary_from_notes(document: dict[str, Any]) -> str:
    notes = document.get("notes")
    if not isinstance(notes, list):
        return ""
    for category in ("summary", "description", "general"):
        for note in notes:
            if not isinstance(note, dict) or note.get("category") != category:
                continue
            text = note.get("text")
            if isinstance(text, str) and text.strip():
                return text.strip()
    return ""


def parse_csaf_document(
    payload: Any,
    *,
    reliability: str,
    document_url: str,
) -> ConnectorRecord:
    if not isinstance(payload, dict):
        raise CSAFAdapterError("CSAF advisory must be a JSON object")
    document = payload.get("document")
    if not isinstance(document, dict):
        raise CSAFAdapterError("CSAF advisory has no document object")
    tracking = document.get("tracking")
    if not isinstance(tracking, dict):
        raise CSAFAdapterError("CSAF advisory has no tracking object")
    advisory_id = tracking.get("id")
    title = document.get("title")
    if not isinstance(advisory_id, str) or not advisory_id.strip():
        raise CSAFAdapterError("CSAF advisory has no tracking id")
    if not isinstance(title, str) or not title.strip():
        raise CSAFAdapterError("CSAF advisory has no title")
    published_at = tracking.get("initial_release_date") or tracking.get("current_release_date")
    if published_at is not None and not isinstance(published_at, str):
        raise CSAFAdapterError("CSAF release date is invalid")
    return ConnectorRecord(
        external_id=advisory_id.strip(),
        object_type="security-advisory",
        title=title.strip(),
        url=document_url,
        summary=_summary_from_notes(document),
        published_at=published_at,
        source_reliability=reliability,
        confidence=96,
        raw=payload,
    )
