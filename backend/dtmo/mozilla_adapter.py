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

MOZILLA_EXECUTION_PROFILE = "mozilla-mfsa-v1"
_MAX_MOZILLA_ADVISORIES = 25
_MFSA_PATH = re.compile(r"^/(?:[a-z]{2}(?:-[A-Z]{2})?/)?security/advisories/(mfsa\d{4}-\d{2,3})/?$", re.IGNORECASE)
_CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)


class _MozillaAdvisoryLinkParser(HTMLParser):
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
        self.links.append((self._href, " ".join("".join(self._text).split())))
        self._href = None
        self._text = []


def _canonical_mfsa_url(href: str) -> tuple[str, str] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme != "https" or parsed.hostname not in {"www.mozilla.org", "mozilla.org"}:
            return None
        path = parsed.path
    else:
        path = href.split("?", 1)[0].split("#", 1)[0]
    match = _MFSA_PATH.fullmatch(path)
    if match is None:
        return None
    advisory_id = match.group(1).lower()
    return advisory_id, f"https://www.mozilla.org/security/advisories/{advisory_id}/"


def discover_mozilla_advisories(payload: bytes) -> list[tuple[str, str, str]]:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Mozilla advisory index is not valid UTF-8 HTML") from exc
    parser = _MozillaAdvisoryLinkParser()
    parser.feed(html)
    discovered: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for href, title in parser.links:
        canonical = _canonical_mfsa_url(href)
        if canonical is None:
            continue
        advisory_id, url = canonical
        if advisory_id in seen:
            continue
        seen.add(advisory_id)
        discovered.append((advisory_id, url, title or advisory_id.upper()))
        if len(discovered) >= _MAX_MOZILLA_ADVISORIES:
            break
    if not discovered:
        raise SourceExecutionError("Mozilla advisory index contained no bounded MFSA links")
    return discovered


def parse_mozilla_advisory(payload: bytes, *, advisory_id: str, url: str, title: str, reliability: str) -> ConnectorRecord:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Mozilla advisory document is not valid UTF-8 HTML") from exc
    text = " ".join(re.sub(r"<[^>]+>", " ", html).split())
    if "mozilla foundation security advisory" not in text.lower():
        raise SourceExecutionError("Mozilla advisory document did not contain the expected MFSA marker")
    cves = sorted({match.upper() for match in _CVE_PATTERN.findall(text)})
    if not cves:
        raise SourceExecutionError("Mozilla advisory document contained no published CVE identifiers")
    return ConnectorRecord(
        external_id=advisory_id.upper(),
        object_type="security-advisory",
        title=title,
        url=url,
        summary=f"Mozilla Foundation Security Advisory covering {len(cves)} published CVE(s)",
        published_at=None,
        source_reliability=reliability,
        confidence=96,
        raw={"advisory_id": advisory_id, "url": url, "title": title, "cves": cves},
    )


async def execute_mozilla_source(source: SourceDefinition, *, timeout_seconds: float = 20.0) -> ConnectorResult:
    started = datetime.now(UTC).isoformat()
    if not source.enabled:
        raise SourceExecutionError("source is disabled")
    try:
        index_payload: Any = await asyncio.to_thread(_fetch_html_sync, source.endpoint_url, timeout=timeout_seconds)
        if not isinstance(index_payload, bytes):
            raise SourceExecutionError("Mozilla adapter requires bounded HTML bytes")
        discovered = discover_mozilla_advisories(index_payload)
        records: list[ConnectorRecord] = []
        for advisory_id, url, title in discovered:
            payload: Any = await asyncio.to_thread(_fetch_html_sync, url, timeout=timeout_seconds)
            if not isinstance(payload, bytes):
                raise SourceExecutionError("Mozilla advisory requires bounded HTML bytes")
            records.append(parse_mozilla_advisory(payload, advisory_id=advisory_id, url=url, title=title, reliability=source.reliability))
    except SourceExecutionError as exc:
        return ConnectorResult(connector_id=source.id, started_at=started, finished_at=datetime.now(UTC).isoformat(), records=[], attempts=1, status="failed", error=str(exc))
    return ConnectorResult(connector_id=source.id, started_at=started, finished_at=datetime.now(UTC).isoformat(), records=records, attempts=1, status="completed")
