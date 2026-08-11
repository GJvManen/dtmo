from __future__ import annotations

import socket

import pytest

from dtmo.source_catalog import SOURCE_CATALOG
from dtmo.source_executor import (
    SUPPORTED_REGISTRY_EXECUTION_PROFILES,
    SourceExecutionError,
    _resolve_public_endpoint,
    parse_registered_source,
)
from dtmo.sources import SourceDefinition


def _source(source_id: str, *, reliability: str = "high") -> SourceDefinition:
    return SourceDefinition(
        id=source_id,
        name=source_id,
        source_type="json-feed",
        endpoint_url="https://example.com/feed.json",
        enabled=True,
        interval_seconds=3600,
        reliability=reliability,
        secret_ref=None,
        created_by="admin",
        updated_by="admin",
    )


def test_catalog_contains_broad_authoritative_source_set() -> None:
    ids = {source.id for source in SOURCE_CATALOG}
    assert {"cisa-kev", "nvd-cve", "github-global-advisories", "ncsc-nl-advisories", "cert-eu-advisories", "msrc-security-update-guide"} <= ids
    assert len(SOURCE_CATALOG) >= 15
    assert all(source.endpoint_url.startswith("https://") for source in SOURCE_CATALOG)


def test_nvd_profile_normalizes_cve_record() -> None:
    source = _source("nvd-cve", reliability="authoritative")
    payload = {
        "vulnerabilities": [
            {
                "cve": {
                    "id": "CVE-2026-12345",
                    "published": "2026-08-10T12:00:00Z",
                    "descriptions": [{"lang": "en", "value": "Example vulnerability"}],
                    "references": [{"url": "https://example.org/advisory"}],
                }
            }
        ]
    }
    records = parse_registered_source(source, payload)
    assert len(records) == 1
    assert records[0].external_id == "CVE-2026-12345"
    assert records[0].summary == "Example vulnerability"
    assert records[0].source_reliability == "authoritative"


def test_github_profile_normalizes_advisory() -> None:
    source = _source("github-global-advisories")
    records = parse_registered_source(
        source,
        [
            {
                "ghsa_id": "GHSA-abcd-1234-5678",
                "cve_id": "CVE-2026-5555",
                "summary": "Dependency vulnerability",
                "description": "Detailed description",
                "html_url": "https://github.com/advisories/GHSA-abcd-1234-5678",
                "published_at": "2026-08-10T10:00:00Z",
            }
        ],
    )
    assert len(records) == 1
    assert records[0].external_id == "GHSA-abcd-1234-5678"
    assert records[0].confidence == 90


def test_unknown_json_source_requires_canonical_dtmo_shape() -> None:
    source = _source("school-cert-custom")
    records = parse_registered_source(
        source,
        {
            "items": [
                {
                    "external_id": "school-cert-1",
                    "title": "Education sector alert",
                    "url": "https://example.org/alerts/1",
                    "summary": "Sector-relevant alert",
                    "confidence": 85,
                }
            ]
        },
    )
    assert records[0].external_id == "school-cert-1"
    with pytest.raises(SourceExecutionError):
        parse_registered_source(source, {"records": []})


def test_runtime_dns_validation_rejects_private_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 443))],
    )
    with pytest.raises(SourceExecutionError, match="non-global"):
        _resolve_public_endpoint("https://example.com/feed.json")


def test_runtime_dns_validation_preserves_path_and_query(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))],
    )
    endpoint = _resolve_public_endpoint("https://example.com/feed.json?limit=10")
    assert endpoint.address == "93.184.216.34"
    assert endpoint.path == "/feed.json?limit=10"


def test_every_supported_catalog_profile_has_a_governed_executor() -> None:
    supported = [entry for entry in SOURCE_CATALOG if entry.execution_status == "supported"]
    assert {entry.execution_profile for entry in supported} == SUPPORTED_REGISTRY_EXECUTION_PROFILES


def test_built_in_catalog_sources_are_explicit_and_separate() -> None:
    built_in = [entry for entry in SOURCE_CATALOG if entry.execution_status == "supported-built-in"]
    assert {(entry.id, entry.execution_profile) for entry in built_in} == {
        ("cisa-kev", "built-in-cisa-kev")
    }
