from __future__ import annotations

import asyncio
import http.client
import ipaddress
import json
import socket
import ssl
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

from defusedxml import ElementTree as ET

from dtmo.connectors.base import ConnectorRecord, ConnectorResult
from dtmo.ncsc_csaf_adapter import CSAFAdapterError, parse_csaf_document, parse_csaf_index
from dtmo.source_catalog import catalog_by_id
from dtmo.sources import SourceDefinition, validate_source_url

MAX_RESPONSE_BYTES = 5 * 1024 * 1024


class SourceExecutionError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ResolvedEndpoint:
    hostname: str
    address: str
    path: str


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, hostname: str, address: str, *, timeout: float) -> None:
        context = ssl.create_default_context()
        super().__init__(hostname, port=443, timeout=timeout, context=context)
        self._validated_address = address
        self._ssl_context = context

    def connect(self) -> None:
        raw = socket.create_connection((self._validated_address, 443), self.timeout)
        self.sock = self._ssl_context.wrap_socket(raw, server_hostname=self.host)


def _resolve_public_endpoint(url: str) -> ResolvedEndpoint:
    validated = validate_source_url(url)
    parsed = urlparse(validated)
    if parsed.hostname is None:
        raise SourceExecutionError("source URL has no hostname")
    hostname = parsed.hostname.rstrip(".").lower()
    try:
        answers = socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise SourceExecutionError("source hostname could not be resolved") from exc
    addresses = sorted({str(answer[4][0]) for answer in answers})
    if not addresses:
        raise SourceExecutionError("source hostname resolved to no addresses")
    for value in addresses:
        try:
            address = ipaddress.ip_address(value)
        except ValueError as exc:
            raise SourceExecutionError("source DNS returned an invalid address") from exc
        if not address.is_global:
            raise SourceExecutionError("source DNS resolved to a non-global address")
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    return ResolvedEndpoint(hostname=hostname, address=addresses[0], path=path)


def _fetch_bounded_sync(
    url: str,
    *,
    timeout: float,
    accept: str,
    allowed_content_types: frozenset[str],
) -> bytes:
    endpoint = _resolve_public_endpoint(url)
    connection = _PinnedHTTPSConnection(endpoint.hostname, endpoint.address, timeout=timeout)
    try:
        connection.request(
            "GET",
            endpoint.path,
            headers={
                "Accept": accept,
                "User-Agent": "DTMO/16.0 registered-source-executor",
                "Connection": "close",
            },
        )
        response = connection.getresponse()
        if 300 <= response.status < 400:
            raise SourceExecutionError("source redirects are not allowed")
        if response.status != 200:
            raise SourceExecutionError(f"source returned HTTP {response.status}")
        content_type = response.getheader("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type not in allowed_content_types:
            raise SourceExecutionError(
                f"source response content type is not allowed: {content_type or 'missing'}"
            )
        declared = response.getheader("Content-Length")
        if declared:
            try:
                if int(declared) > MAX_RESPONSE_BYTES:
                    raise SourceExecutionError("source response exceeds size limit")
            except ValueError as exc:
                raise SourceExecutionError("source returned invalid content length") from exc
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise SourceExecutionError("source response exceeds size limit")
        return body
    finally:
        connection.close()


def _fetch_json_sync(url: str, *, timeout: float) -> Any:
    body = _fetch_bounded_sync(
        url,
        timeout=timeout,
        accept="application/json, application/*+json",
        allowed_content_types=frozenset({"application/json", "text/json"}),
    )
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SourceExecutionError("source response is not valid UTF-8 JSON") from exc


def _fetch_text_sync(url: str, *, timeout: float) -> bytes:
    return _fetch_bounded_sync(
        url,
        timeout=timeout,
        accept="text/plain",
        allowed_content_types=frozenset({"text/plain"}),
    )


def _fetch_rss_sync(url: str, *, timeout: float) -> bytes:
    return _fetch_bounded_sync(
        url,
        timeout=timeout,
        accept="application/rss+xml, application/xml, text/xml",
        allowed_content_types=frozenset({"application/rss+xml", "application/xml", "text/xml"}),
    )


def _english_description(descriptions: Any) -> str:
    if not isinstance(descriptions, list):
        return ""
    for item in descriptions:
        if isinstance(item, dict) and item.get("lang") == "en" and isinstance(item.get("value"), str):
            return str(item["value"])
    return ""


def _parse_nvd(payload: Any, reliability: str) -> list[ConnectorRecord]:
    if not isinstance(payload, dict) or not isinstance(payload.get("vulnerabilities"), list):
        raise SourceExecutionError("NVD response has no vulnerabilities list")
    records: list[ConnectorRecord] = []
    for wrapper in payload["vulnerabilities"]:
        if not isinstance(wrapper, dict) or not isinstance(wrapper.get("cve"), dict):
            continue
        cve = wrapper["cve"]
        cve_id = str(cve.get("id", "")).strip()
        if not cve_id:
            continue
        references = cve.get("references")
        url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        if isinstance(references, list):
            first = next(
                (
                    entry.get("url")
                    for entry in references
                    if isinstance(entry, dict) and isinstance(entry.get("url"), str)
                ),
                None,
            )
            if isinstance(first, str):
                url = first
        records.append(
            ConnectorRecord(
                external_id=cve_id,
                object_type="vulnerability",
                title=cve_id,
                url=url,
                summary=_english_description(cve.get("descriptions")),
                published_at=str(cve.get("published")) if cve.get("published") else None,
                source_reliability=reliability,
                confidence=94,
                raw=cve,
            )
        )
    return records


def _parse_github(payload: Any, reliability: str) -> list[ConnectorRecord]:
    if not isinstance(payload, list):
        raise SourceExecutionError("GitHub advisory response must be a list")
    records: list[ConnectorRecord] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        external_id = str(item.get("ghsa_id") or item.get("cve_id") or "").strip()
        if not external_id:
            continue
        url = str(item.get("html_url") or f"https://github.com/advisories/{external_id}")
        records.append(
            ConnectorRecord(
                external_id=external_id,
                object_type="vulnerability",
                title=str(item.get("summary") or external_id),
                url=url,
                summary=str(item.get("description") or item.get("summary") or ""),
                published_at=str(item.get("published_at")) if item.get("published_at") else None,
                source_reliability=reliability,
                confidence=90,
                raw=item,
            )
        )
    return records


def _parse_dtmo_json(payload: Any, reliability: str) -> list[ConnectorRecord]:
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise SourceExecutionError("generic JSON feed must expose an items list")
    records: list[ConnectorRecord] = []
    for item in payload["items"]:
        if not isinstance(item, dict):
            continue
        external_id = str(item.get("external_id", "")).strip()
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        if not external_id or not title or not url:
            raise SourceExecutionError("generic JSON item requires external_id, title and url")
        confidence_value = item.get("confidence", 80)
        if not isinstance(confidence_value, int) or not 0 <= confidence_value <= 100:
            raise SourceExecutionError("generic JSON confidence must be an integer from 0 to 100")
        records.append(
            ConnectorRecord(
                external_id=external_id,
                object_type=str(item.get("object_type") or "threat-intelligence"),
                title=title,
                url=url,
                summary=str(item.get("summary") or ""),
                published_at=str(item.get("published_at")) if item.get("published_at") else None,
                source_reliability=reliability,
                confidence=confidence_value,
                raw=item,
            )
        )
    return records


def _rss_text(item: Any, tag: str) -> str:
    child = item.find(tag)
    return "" if child is None or child.text is None else child.text.strip()


def _parse_rss(payload: bytes, reliability: str) -> list[ConnectorRecord]:
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise SourceExecutionError("RSS response is not valid XML") from exc
    items = root.findall("./channel/item")
    if not items:
        raise SourceExecutionError("RSS response has no channel items")
    records: list[ConnectorRecord] = []
    for item in items:
        title = _rss_text(item, "title")
        link = _rss_text(item, "link")
        guid = _rss_text(item, "guid") or link
        if not title or not link or not guid:
            continue
        records.append(
            ConnectorRecord(
                external_id=guid,
                object_type="security-advisory",
                title=title,
                url=link,
                summary=_rss_text(item, "description"),
                published_at=_rss_text(item, "pubDate") or None,
                source_reliability=reliability,
                confidence=92,
                raw={
                    "guid": guid,
                    "title": title,
                    "link": link,
                    "description": _rss_text(item, "description"),
                    "pubDate": _rss_text(item, "pubDate"),
                },
            )
        )
    if not records:
        raise SourceExecutionError("RSS response contained no usable advisory items")
    return records


def parse_registered_source(source: SourceDefinition, payload: Any) -> list[ConnectorRecord]:
    catalog = catalog_by_id(source.id)
    profile = (
        catalog.execution_profile
        if catalog and catalog.execution_status == "supported"
        else "dtmo-json-v1"
    )
    if profile == "nvd-cve-v2":
        return _parse_nvd(payload, source.reliability)
    if profile == "github-global-advisories-v1":
        return _parse_github(payload, source.reliability)
    if profile == "rss-2.0":
        if not isinstance(payload, bytes):
            raise SourceExecutionError("RSS adapter requires bounded XML bytes")
        return _parse_rss(payload, source.reliability)
    return _parse_dtmo_json(payload, source.reliability)


def _execute_ncsc_csaf_sync(source: SourceDefinition, *, timeout: float) -> list[ConnectorRecord]:
    base = source.endpoint_url.rstrip("/")
    index_url = f"{base}/v2/index.txt"
    try:
        paths = parse_csaf_index(_fetch_text_sync(index_url, timeout=timeout))
    except CSAFAdapterError as exc:
        raise SourceExecutionError(str(exc)) from exc
    records: list[ConnectorRecord] = []
    for path in paths:
        document_url = f"{base}/v2/{path}"
        payload = _fetch_json_sync(document_url, timeout=timeout)
        try:
            record = parse_csaf_document(
                payload,
                reliability=source.reliability,
                document_url=document_url,
            )
        except CSAFAdapterError as exc:
            raise SourceExecutionError(str(exc)) from exc
        records.append(record)
    if not records:
        raise SourceExecutionError("CSAF distribution produced no advisory records")
    return records


async def execute_registered_source(
    source: SourceDefinition, *, timeout_seconds: float = 20.0
) -> ConnectorResult:
    started = datetime.now(UTC).isoformat()
    if source.source_type != "json-feed":
        raise SourceExecutionError("only governed registry feeds use the generic executor")
    if not source.enabled:
        raise SourceExecutionError("source is disabled")
    try:
        catalog = catalog_by_id(source.id)
        profile = (
            catalog.execution_profile
            if catalog and catalog.execution_status == "supported"
            else "dtmo-json-v1"
        )
        if profile == "csaf-2.0":
            records = await asyncio.to_thread(
                _execute_ncsc_csaf_sync, source, timeout=timeout_seconds
            )
        elif profile == "rss-2.0":
            payload = await asyncio.to_thread(
                _fetch_rss_sync, source.endpoint_url, timeout=timeout_seconds
            )
            records = parse_registered_source(source, payload)
        else:
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
