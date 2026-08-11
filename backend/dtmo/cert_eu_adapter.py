from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlparse

from dtmo.connectors.base import ConnectorRecord

MAX_CERT_EU_ADVISORIES = 25
_ADVISORY_PATH = re.compile(r"^/publications/security-advisories/(?P<serial>\d{4}-\d{3})/?$")
_TAGS = re.compile(r"<[^>]+>")


class CERTEUAdapterError(ValueError):
    pass


class _AdvisoryLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.paths: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        href = next((value for key, value in attrs if key.lower() == "href"), None)
        if not href:
            return
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
            return
        if _ADVISORY_PATH.fullmatch(parsed.path):
            self.paths.append(parsed.path.rstrip("/"))


def parse_cert_eu_listing(payload: bytes, *, expected_year: str) -> list[str]:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CERTEUAdapterError("CERT-EU advisory listing is not valid UTF-8") from exc
    parser = _AdvisoryLinkParser()
    parser.feed(text)
    prefix = f"{expected_year}-"
    paths: list[str] = []
    seen: set[str] = set()
    for path in parser.paths:
        match = _ADVISORY_PATH.fullmatch(path)
        if match is None or not match.group("serial").startswith(prefix) or path in seen:
            continue
        seen.add(path)
        paths.append(path)
        if len(paths) >= MAX_CERT_EU_ADVISORIES:
            break
    if not paths:
        raise CERTEUAdapterError("CERT-EU listing exposed no bounded advisory links for the expected year")
    return paths


def _plain_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(html.unescape(_TAGS.sub(" ", value)).split())


def parse_cert_eu_document(
    payload: Any,
    *,
    reliability: str,
    document_url: str,
) -> ConnectorRecord:
    if not isinstance(payload, dict):
        raise CERTEUAdapterError("CERT-EU advisory JSON must be an object")
    serial = str(payload.get("serial_number") or "").strip()
    title = str(payload.get("title") or "").strip()
    publish_date = str(payload.get("publish_date") or "").strip()
    if not re.fullmatch(r"\d{4}-\d{3}", serial):
        raise CERTEUAdapterError("CERT-EU advisory JSON has no valid serial number")
    if not title or not publish_date:
        raise CERTEUAdapterError("CERT-EU advisory JSON requires title and publish date")
    expected_path = f"/publications/security-advisories/{serial}/json"
    parsed_url = urlparse(document_url)
    if parsed_url.path.rstrip("/") != expected_path:
        raise CERTEUAdapterError("CERT-EU advisory JSON URL does not match its serial number")
    advisory_url = document_url.removesuffix("/json")
    summary = _plain_text(payload.get("description"))
    if not summary:
        summary = _plain_text(payload.get("content_markdown"))[:2000]
    return ConnectorRecord(
        external_id=f"CERT-EU-SA-{serial}",
        object_type="security-advisory",
        title=title,
        url=advisory_url,
        summary=summary,
        published_at=publish_date,
        source_reliability=reliability,
        confidence=93,
        raw=payload,
    )
