from __future__ import annotations

import asyncio
import re
from datetime import UTC, datetime
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlparse

from dtmo.connectors.base import ConnectorRecord, ConnectorResult
from dtmo.source_executor import SourceExecutionError, _fetch_html_sync
from dtmo.sources import SourceDefinition

BROADCOM_VMWARE_EXECUTION_PROFILE = "broadcom-vmware-vmsa-v1"
_MAX_VMSA_ADVISORIES = 25
_VMSA_PATTERN = re.compile(r"VMSA-\d{4}-\d{4}(?:\.\d+)?", re.IGNORECASE)
_CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
_ALLOWED_DETAIL_HOST = "support.broadcom.com"
_ALLOWED_DETAIL_PATH = re.compile(
    r"^/web/ecx/support-content-notification/-/external/content/securityadvisories(?:/|$)",
    re.IGNORECASE,
)


class _BroadcomLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        values = {key.lower(): value for key, value in attrs}
        self._href = values.get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self._href is None:
            return
        title = " ".join("".join(self._text).split())
        self.links.append((self._href, title))
        self._href = None
        self._text = []


def _canonical_vmsa_detail_url(href: str, *, index_url: str) -> str | None:
    absolute = urljoin(index_url, href)
    parsed = urlparse(absolute)
    if parsed.scheme != "https" or parsed.hostname != _ALLOWED_DETAIL_HOST:
        return None
    if _ALLOWED_DETAIL_PATH.match(parsed.path) is None:
        return None
    return f"https://{_ALLOWED_DETAIL_HOST}{parsed.path}"


def discover_broadcom_vmware_advisories(
    payload: bytes, *, index_url: str
) -> list[tuple[str, str, str]]:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Broadcom VMware advisory index is not valid UTF-8 HTML") from exc
    parser = _BroadcomLinkParser()
    parser.feed(html)
    discovered: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for href, title in parser.links:
        advisory_match = _VMSA_PATTERN.search(title)
        if advisory_match is None:
            advisory_match = _VMSA_PATTERN.search(href)
        if advisory_match is None:
            continue
        url = _canonical_vmsa_detail_url(href, index_url=index_url)
        if url is None:
            continue
        advisory_id = advisory_match.group(0).upper()
        if advisory_id in seen:
            continue
        seen.add(advisory_id)
        discovered.append((advisory_id, url, title or advisory_id))
        if len(discovered) >= _MAX_VMSA_ADVISORIES:
            break
    if not discovered:
        raise SourceExecutionError("Broadcom VMware advisory index contained no bounded VMSA links")
    return discovered


def parse_broadcom_vmware_advisory(
    payload: bytes, *, advisory_id: str, url: str, discovery_title: str, reliability: str
) -> ConnectorRecord:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Broadcom VMware advisory is not valid UTF-8 HTML") from exc
    text = " ".join(re.sub(r"<[^>]+>", " ", html).split())
    if advisory_id.lower() not in text.lower():
        raise SourceExecutionError("Broadcom VMware advisory identifier mismatch")
    cves = sorted({value.upper() for value in _CVE_PATTERN.findall(text)})
    if not cves:
        raise SourceExecutionError("Broadcom VMware advisory contained no published CVE identifiers")
    title = discovery_title.strip() or advisory_id
    return ConnectorRecord(
        external_id=advisory_id,
        object_type="security-advisory",
        title=title,
        url=url,
        summary=f"Broadcom VMware security advisory covering {len(cves)} published CVE(s)",
        published_at=None,
        source_reliability=reliability,
        confidence=96,
        raw={
            "advisory_id": advisory_id,
            "url": url,
            "discovery_title": title,
            "cves": cves,
        },
    )


async def execute_broadcom_vmware_source(
    source: SourceDefinition, *, timeout_seconds: float = 20.0
) -> ConnectorResult:
    started = datetime.now(UTC).isoformat()
    if not source.enabled:
        raise SourceExecutionError("source is disabled")
    try:
        index_payload: Any = await asyncio.to_thread(
            _fetch_html_sync, source.endpoint_url, timeout=timeout_seconds
        )
        if not isinstance(index_payload, bytes):
            raise SourceExecutionError("Broadcom VMware adapter requires bounded HTML bytes")
        discovered = discover_broadcom_vmware_advisories(
            index_payload, index_url=source.endpoint_url
        )
        records: list[ConnectorRecord] = []
        for advisory_id, url, title in discovered:
            payload: Any = await asyncio.to_thread(
                _fetch_html_sync, url, timeout=timeout_seconds
            )
            if not isinstance(payload, bytes):
                raise SourceExecutionError("Broadcom VMware advisory requires bounded HTML bytes")
            records.append(
                parse_broadcom_vmware_advisory(
                    payload,
                    advisory_id=advisory_id,
                    url=url,
                    discovery_title=title,
                    reliability=source.reliability,
                )
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
