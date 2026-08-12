from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from dtmo.connectors.base import ConnectorResult
from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import SourceExecutionError, _fetch_json_sync, parse_registered_source
from dtmo.sources import SourceDefinition


async def test_manual_source(
    source: SourceDefinition, *, timeout_seconds: float = 20.0
) -> ConnectorResult:
    """Test a disabled manual DTMO JSON source without ingesting or changing state.

    This path exists only for pre-activation onboarding. Code-reviewed catalog
    profiles keep using their dedicated adapters and normal execution contracts.
    """
    started = datetime.now(UTC).isoformat()
    if source.source_type != "json-feed":
        raise SourceExecutionError("pre-activation test supports manual JSON feeds only")
    catalog = catalog_by_id(source.id)
    if catalog is not None and catalog.execution_status == "supported":
        raise SourceExecutionError(
            "code-reviewed catalog sources must use their governed adapter execution path"
        )
    try:
        payload = await asyncio.to_thread(
            _fetch_json_sync, source.endpoint_url, timeout=timeout_seconds
        )
        records = parse_registered_source(source, payload)
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
