from __future__ import annotations

import asyncio
import re
from datetime import UTC, datetime
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlparse

from dtmo.connectors.base import ConnectorRecord, ConnectorResult
from dtmo.source_executor import SourceExecutionError, _fetch_html_sync
from dtmo.sources import SourceDefinition

FORTINET_EXECUTION_PROFILE = "fortinet-psirt-v1"
_MAX_FORTINET_ADVISORIES = 25
_FORTINET_PATH = re.compile(r"^/psirt/(FG-IR-\d{2}-\d{3,4})/?$", re.IGNORECASE)
_CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)


class _FortinetLinkParser(HTMLParser):
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


def _canonical_fortinet_advisory_url(href: str) -> tuple[str, str] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme != "https" or parsed.hostname not in {"fortiguard.com", "www.fortiguard.com"}:
            return None
        path = parsed.path
    else:
        path = href.split("?", 1)[0].split("#", 1)[0]
    match = _FORTINET_PATH.fullmatch(path)
    if match is None:
        return None
    advisory_id = match.group(1).upper()
    return advisory_id, f"https://www.fortiguard.com/psirt/{advisory_id}"


def discover_fortinet_advisories(payload: bytes) -> list[tuple[str, str, str]]:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Fortinet PSIRT index is not valid UTF-8 HTML") from exc
    parser = _FortinetLinkParser()
    parser.feed(html)
    discovered: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for href, title in parser.links:
        canonical = _canonical_fortinet_advisory_url(href)
        if canonical is None:
            continue
        advisory_id, url = canonical
        if advisory_id in seen:
            continue
        seen.add(advisory_id)
        discovered.append((advisory_id, url, title or advisory_id))
        if len(discovered) >= _MAX_FORTINET_ADVISORIES:
            break
    if not discovered:
        raise SourceExecutionError("Fortinet PSIRT index contained no bounded advisory links")
    return discovered


def parse_fortinet_advisory(
    payload: bytes, *, advisory_id: str, url: str, discovery_title: str, reliability: str
) -> ConnectorRecord:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Fortinet PSIRT advisory is not valid UTF-8 HTML") from exc
    text = " ".join(re.sub(r"<[^>]+>", " ", html).split())
    if advisory_id.lower() not in text.lower():
        raise SourceExecutionError("Fortinet PSIRT advisory identifier mismatch")
    cves = sorted({value.upper() for value in _CVE_PATTERN.findall(text)})
    if not cves:
        raise SourceExecutionError("Fortinet PSIRT advisory contained no published CVE identifiers")
    title = discovery_title.strip() or advisory_id
    return ConnectorRecord(
        external_id=advisory_id,
        object_type="security-advisory",
        title=title,
        url=url,
        summary=f"Fortinet PSIRT advisory covering {len(cves)} published CVE(s)",
        published_at=None,
        source_reliability=reliability,
        confidence=96,
        raw={"advisory_id": advisory_id, "url": url, "discovery_title": title, "cves": cves},
    )


async def execute_fortinet_source(
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
            raise SourceExecutionError("Fortinet PSIRT adapter requires bounded HTML bytes")
        discovered = discover_fortinet_advisories(index_payload)
        records: list[ConnectorRecord] = []
        for advisory_id, url, title in discovered:
            payload: Any = await asyncio.to_thread(_fetch_html_sync, url, timeout=timeout_seconds)
            if not isinstance(payload, bytes):
                raise SourceExecutionError("Fortinet PSIRT advisory requires bounded HTML bytes")
            records.append(
                parse_fortinet_advisory(
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
