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

APPLE_EXECUTION_PROFILE = "apple-security-releases-v1"
_MAX_APPLE_RELEASES = 25
_APPLE_ARTICLE_PATH = re.compile(r"^/(?:[a-z]{2}-[a-z]{2}/)?(\d{6})/?$")
_INDEX_ARTICLE_ID = "100100"


class _AppleReleaseLinkParser(HTMLParser):
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


def _canonical_apple_article_url(href: str) -> tuple[str, str] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme != "https" or parsed.hostname != "support.apple.com":
            return None
        path = parsed.path
    else:
        path = href.split("?", 1)[0].split("#", 1)[0]
    match = _APPLE_ARTICLE_PATH.fullmatch(path)
    if match is None:
        return None
    article_id = match.group(1)
    if article_id == _INDEX_ARTICLE_ID:
        return None
    return article_id, f"https://support.apple.com/{article_id}"


def parse_apple_security_release_index(payload: bytes, reliability: str) -> list[ConnectorRecord]:
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceExecutionError("Apple Security Releases index is not valid UTF-8 HTML") from exc
    parser = _AppleReleaseLinkParser()
    parser.feed(html)

    records: list[ConnectorRecord] = []
    seen: set[str] = set()
    for href, title in parser.links:
        canonical = _canonical_apple_article_url(href)
        if canonical is None:
            continue
        article_id, url = canonical
        if article_id in seen or not title:
            continue
        lowered = title.lower()
        if "security" not in lowered and "beveilig" not in lowered:
            continue
        seen.add(article_id)
        records.append(
            ConnectorRecord(
                external_id=f"APPLE-{article_id}",
                object_type="security-advisory",
                title=title,
                url=url,
                summary="Apple Product Security release notice",
                published_at=None,
                source_reliability=reliability,
                confidence=96,
                raw={"article_id": article_id, "href": href, "title": title},
            )
        )
        if len(records) >= _MAX_APPLE_RELEASES:
            break
    if not records:
        raise SourceExecutionError("Apple Security Releases index contained no usable security-content links")
    return records


async def execute_apple_source(
    source: SourceDefinition, *, timeout_seconds: float = 20.0
) -> ConnectorResult:
    started = datetime.now(UTC).isoformat()
    if not source.enabled:
        raise SourceExecutionError("source is disabled")
    try:
        payload: Any = await asyncio.to_thread(
            _fetch_html_sync, source.endpoint_url, timeout=timeout_seconds
        )
        if not isinstance(payload, bytes):
            raise SourceExecutionError("Apple Security Releases adapter requires bounded HTML bytes")
        records = parse_apple_security_release_index(payload, source.reliability)
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
