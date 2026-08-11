from __future__ import annotations

import asyncio

import pytest

from dtmo.apple_adapter import APPLE_EXECUTION_PROFILE, parse_apple_security_release_index
from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import SourceExecutionError
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY, execute_source
from dtmo.sources import SourceDefinition


def _apple_source() -> SourceDefinition:
    return SourceDefinition(
        id="apple-security-releases",
        name="Apple Security Releases",
        source_type="json-feed",
        endpoint_url="https://support.apple.com/100100",
        enabled=True,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=None,
        created_by="admin",
        updated_by="admin",
    )


def test_apple_catalog_is_connected_through_framework() -> None:
    entry = catalog_by_id("apple-security-releases")
    assert entry is not None
    assert entry.execution_status == "supported"
    assert entry.execution_profile == APPLE_EXECUTION_PROFILE
    spec = SOURCE_ADAPTER_REGISTRY.get(APPLE_EXECUTION_PROFILE)
    assert spec is not None
    assert spec.execution_kind == "anonymous"
    assert spec.requires_secret is False


def test_apple_index_normalizes_only_first_party_security_content_links() -> None:
    payload = b"""
    <html><body>
      <a href="/100100">Apple security releases</a>
      <a href="/127594">About the security content of iOS 26.5.2 and iPadOS 26.5.2</a>
      <a href="https://support.apple.com/en-us/127110">About the security content of iOS 26.5 and iPadOS 26.5</a>
      <a href="https://evil.example/127999">About the security content of fakeOS</a>
      <a href="/127777">How to update iPhone</a>
    </body></html>
    """
    records = parse_apple_security_release_index(payload, "authoritative")
    assert [record.external_id for record in records] == ["APPLE-127594", "APPLE-127110"]
    assert records[0].url == "https://support.apple.com/127594"
    assert records[0].source_reliability == "authoritative"
    assert records[0].raw["article_id"] == "127594"


def test_apple_index_fails_closed_when_no_usable_security_links_exist() -> None:
    with pytest.raises(SourceExecutionError, match="no usable"):
        parse_apple_security_release_index(
            b'<html><body><a href="https://example.org/127594">security content</a></body></html>',
            "authoritative",
        )


def test_framework_dispatches_apple_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = b'<a href="/127594">About the security content of iOS 26.5.2 and iPadOS 26.5.2</a>'

    def fake_fetch(url: str, *, timeout: float) -> bytes:
        assert url == "https://support.apple.com/100100"
        assert timeout == 20.0
        return payload

    monkeypatch.setattr("dtmo.apple_adapter._fetch_html_sync", fake_fetch)
    result = asyncio.run(execute_source(_apple_source()))
    assert result.status == "completed"
    assert result.records[0].external_id == "APPLE-127594"
