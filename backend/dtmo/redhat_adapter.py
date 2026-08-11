from __future__ import annotations

import asyncio
import re
from datetime import UTC, datetime
from typing import Any

from dtmo.connectors.base import ConnectorRecord, ConnectorResult
from dtmo.ncsc_csaf_adapter import CSAFAdapterError, parse_csaf_document
from dtmo.source_executor import SourceExecutionError, _fetch_json_sync
from dtmo.sources import SourceDefinition

REDHAT_EXECUTION_PROFILE = "redhat-csaf-v1"
_MAX_RED_HAT_DOCUMENTS = 25
_RHSA_ID = re.compile(r"^RHSA-\d{4}:\d+$")


def parse_redhat_csaf_ids(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        raise SourceExecutionError("Red Hat CSAF index must be a list")
    identifiers: list[str] = []
    seen: set[str] = set()
    for item in payload:
        if not isinstance(item, dict):
            continue
        candidate = next(
            (
                str(item[key]).strip()
                for key in ("RHSA", "rhsa", "id", "ID", "advisory")
                if key in item and item[key] is not None
            ),
            "",
        )
        if not _RHSA_ID.fullmatch(candidate) or candidate in seen:
            continue
        seen.add(candidate)
        identifiers.append(candidate)
        if len(identifiers) >= _MAX_RED_HAT_DOCUMENTS:
            break
    if not identifiers:
        raise SourceExecutionError("Red Hat CSAF index contained no usable RHSA identifiers")
    return identifiers


def _execute_redhat_sync(source: SourceDefinition, *, timeout: float) -> list[ConnectorRecord]:
    base = source.endpoint_url.rstrip("/")
    index_url = (
        f"{base}/csaf.json?created_days_ago=10&per_page={_MAX_RED_HAT_DOCUMENTS}"
        "&isCompressed=false"
    )
    identifiers = parse_redhat_csaf_ids(_fetch_json_sync(index_url, timeout=timeout))
    records: list[ConnectorRecord] = []
    for rhsa_id in identifiers:
        document_url = f"{base}/csaf/{rhsa_id}.json?isCompressed=false"
        payload = _fetch_json_sync(document_url, timeout=timeout)
        try:
            record = parse_csaf_document(
                payload,
                reliability=source.reliability,
                document_url=document_url,
            )
        except CSAFAdapterError as exc:
            raise SourceExecutionError(str(exc)) from exc
        if record.external_id != rhsa_id:
            raise SourceExecutionError("Red Hat CSAF tracking ID does not match requested RHSA")
        records.append(record)
    if not records:
        raise SourceExecutionError("Red Hat CSAF distribution produced no advisory records")
    return records


async def execute_redhat_source(
    source: SourceDefinition, *, timeout_seconds: float = 20.0
) -> ConnectorResult:
    started = datetime.now(UTC).isoformat()
    if not source.enabled:
        raise SourceExecutionError("source is disabled")
    try:
        records = await asyncio.to_thread(
            _execute_redhat_sync,
            source,
            timeout=timeout_seconds,
        )
    except SourceExecutionError as exc:
        return ConnectorResult(
            connector_id=source.id,
            started_at=started,
            finished_at=datetime.now(UTC).isoformat(),
            records=[],
            attempts=1,
            status="failed",
            error=str(exc),
        )
    return ConnectorResult(
        connector_id=source.id,
        started_at=started,
        finished_at=datetime.now(UTC).isoformat(),
        records=records,
        attempts=1,
        status="completed",
    )
