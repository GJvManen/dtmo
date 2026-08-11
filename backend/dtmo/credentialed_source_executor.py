from __future__ import annotations

import asyncio
import json
import os
import re
from datetime import UTC, datetime
from typing import Any

from dtmo.connectors.base import ConnectorRecord, ConnectorResult
from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import MAX_RESPONSE_BYTES, SourceExecutionError, _PinnedHTTPSConnection, _resolve_public_endpoint
from dtmo.sources import SourceDefinition

CREDENTIALED_EXECUTION_PROFILES = frozenset({"cisco-openvuln-v2"})
_SECRET_REF = re.compile(r"^env:([A-Z][A-Z0-9_]*)$")


def _resolve_secret(secret_ref: str | None) -> str:
    if not secret_ref:
        raise SourceExecutionError("credentialed source requires a secret reference")
    match = _SECRET_REF.fullmatch(secret_ref)
    if match is None:
        raise SourceExecutionError("unsupported source secret reference")
    value = os.environ.get(match.group(1), "").strip()
    if not value:
        raise SourceExecutionError("source credential is not available at runtime")
    return value


def _fetch_json_bearer_sync(url: str, *, token: str, timeout: float) -> Any:
    endpoint = _resolve_public_endpoint(url)
    connection = _PinnedHTTPSConnection(endpoint.hostname, endpoint.address, timeout=timeout)
    try:
        connection.request(
            "GET",
            endpoint.path,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "User-Agent": "DTMO/16.0 credentialed-source-executor",
                "Connection": "close",
            },
        )
        response = connection.getresponse()
        if 300 <= response.status < 400:
            raise SourceExecutionError("source redirects are not allowed")
        if response.status != 200:
            raise SourceExecutionError(f"credentialed source returned HTTP {response.status}")
        content_type = response.getheader("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type not in {"application/json", "text/json"}:
            raise SourceExecutionError("credentialed source response content type is not JSON")
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise SourceExecutionError("credentialed source response exceeds size limit")
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SourceExecutionError("credentialed source response is not valid UTF-8 JSON") from exc
    finally:
        connection.close()


def _cisco_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict) and isinstance(payload.get("advisories"), list):
        items = payload["advisories"]
    else:
        raise SourceExecutionError("Cisco OpenVuln response has no advisories list")
    return [item for item in items if isinstance(item, dict)]


def parse_cisco_openvuln(payload: Any, *, reliability: str) -> list[ConnectorRecord]:
    records: list[ConnectorRecord] = []
    for item in _cisco_items(payload)[:25]:
        advisory_id = str(item.get("advisoryId") or "").strip()
        title = str(item.get("advisoryTitle") or "").strip()
        publication_url = str(item.get("publicationUrl") or "").strip()
        if not advisory_id.startswith("cisco-sa-") or not title or not publication_url.startswith("https://"):
            continue
        records.append(
            ConnectorRecord(
                external_id=advisory_id,
                object_type="security-advisory",
                title=title,
                url=publication_url,
                summary=str(item.get("summary") or ""),
                published_at=str(item.get("firstPublished")) if item.get("firstPublished") else None,
                source_reliability=reliability,
                confidence=95,
                raw=item,
            )
        )
    if not records:
        raise SourceExecutionError("Cisco OpenVuln response contained no usable advisories")
    return records


def _execute_cisco_sync(source: SourceDefinition, *, timeout: float) -> list[ConnectorRecord]:
    token = _resolve_secret(source.secret_ref)
    url = f"{source.endpoint_url.rstrip('/')}/latest/25?summaryDetails=true&productNames=true"
    payload = _fetch_json_bearer_sync(url, token=token, timeout=timeout)
    return parse_cisco_openvuln(payload, reliability=source.reliability)


async def execute_credentialed_source(
    source: SourceDefinition, *, timeout_seconds: float = 20.0
) -> ConnectorResult:
    started = datetime.now(UTC).isoformat()
    if not source.enabled:
        raise SourceExecutionError("source is disabled")
    catalog = catalog_by_id(source.id)
    profile = catalog.execution_profile if catalog and catalog.execution_status == "supported" else ""
    if profile not in CREDENTIALED_EXECUTION_PROFILES:
        raise SourceExecutionError("source has no credentialed execution profile")
    try:
        if profile == "cisco-openvuln-v2":
            records = await asyncio.to_thread(_execute_cisco_sync, source, timeout=timeout_seconds)
        else:
            raise SourceExecutionError("credentialed source profile is not implemented")
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
