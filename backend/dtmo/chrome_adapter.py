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

CHROME_EXECUTION_PROFILE = "chrome-security-releases-v1"
_MAX_CHROME_RELEASES = 20
_CHROME_POST_PATH = re.compile(r"^/(\d{4})/(\d{2})/([a-z0-9_-]+)\.html$")
_CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)


class _ChromeReleaseLinkParser(HTMLParser):
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


def _canonical_chrome_post_url(href: str) -> tuple[str, str] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme != "https" or parsed.hostname != "chromereleases.googleblog.com":
            return None
        path = parsed.path
    else:
        path = href.split("?", 1)[0].split("#", 1)[0]
    match = _CHROME_POST_PATH.fullmatch(path)
    if match is None:
        return None
    slug = match.group(3)
    return slug, f"https://chromereleases.googleblog.com{path}"


def discover_chrome_stable_posts(payload: bytes) -> list[tuple[str, str, str]]:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Chrome Releases index is not valid UTF-8 HTML") from exc
    parser = _ChromeReleaseLinkParser()
    parser.feed(html)
    discovered: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for href, title in parser.links:
        canonical = _canonical_chrome_post_url(href)
        if canonical is None or not title:
            continue
        slug, url = canonical
        lowered = title.lower()
        if "stable" not in lowered or "update" not in lowered:
            continue
        if slug in seen:
            continue
        seen.add(slug)
        discovered.append((slug, url, title))
        if len(discovered) >= _MAX_CHROME_RELEASES:
            break
    if not discovered:
        raise SourceExecutionError("Chrome Releases index contained no bounded stable-channel posts")
    return discovered


def parse_chrome_security_post(
    payload: bytes, *, slug: str, url: str, title: str, reliability: str
) -> ConnectorRecord | None:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Chrome release post is not valid UTF-8 HTML") from exc
    text = " ".join(re.sub(r"<[^>]+>", " ", html).split())
    if "security fixes" not in text.lower():
        return None
    cves = sorted({match.upper() for match in _CVE_PATTERN.findall(text)})
    if not cves:
        return None
    return ConnectorRecord(
        external_id=f"CHROME-{slug}",
        object_type="security-advisory",
        title=title,
        url=url,
        summary=f"Google Chrome stable security update covering {len(cves)} published CVE(s)",
        published_at=None,
        source_reliability=reliability,
        confidence=96,
        raw={"slug": slug, "url": url, "title": title, "cves": cves},
    )


async def execute_chrome_source(
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
            raise SourceExecutionError("Chrome Releases adapter requires bounded HTML bytes")
        discovered = discover_chrome_stable_posts(index_payload)
        records: list[ConnectorRecord] = []
        for slug, url, title in discovered:
            payload: Any = await asyncio.to_thread(
                _fetch_html_sync, url, timeout=timeout_seconds
            )
            if not isinstance(payload, bytes):
                raise SourceExecutionError("Chrome release post requires bounded HTML bytes")
            record = parse_chrome_security_post(
                payload,
                slug=slug,
                url=url,
                title=title,
                reliability=source.reliability,
            )
            if record is not None:
                records.append(record)
        if not records:
            raise SourceExecutionError("Chrome stable release discovery contained no posts with published CVEs")
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
