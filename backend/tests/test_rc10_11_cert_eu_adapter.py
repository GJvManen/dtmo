from __future__ import annotations

import pytest

from dtmo.cert_eu_adapter import (
    CERTEUAdapterError,
    MAX_CERT_EU_ADVISORIES,
    parse_cert_eu_document,
    parse_cert_eu_listing,
)
from dtmo.source_catalog import catalog_by_id


def test_cert_eu_catalog_source_is_executable() -> None:
    source = catalog_by_id("cert-eu-advisories")
    assert source is not None
    assert source.execution_status == "supported"
    assert source.execution_profile == "cert-eu-advisories-v1"
    assert source.endpoint_url == "https://cert.europa.eu/publications/security-advisories/2026"


def test_cert_eu_listing_accepts_only_bounded_same_year_relative_advisory_paths() -> None:
    links = "".join(
        f'<a href="/publications/security-advisories/2026-{index:03d}/">item</a>'
        for index in range(1, MAX_CERT_EU_ADVISORIES + 5)
    )
    payload = (
        "<html><body>"
        '<a href="https://evil.example/publications/security-advisories/2026-999/">evil</a>'
        '<a href="/publications/security-advisories/2025-999/">old</a>'
        + links
        + "</body></html>"
    ).encode()
    paths = parse_cert_eu_listing(payload, expected_year="2026")
    assert len(paths) == MAX_CERT_EU_ADVISORIES
    assert paths[0] == "/publications/security-advisories/2026-001"
    assert all(path.startswith("/publications/security-advisories/2026-") for path in paths)


def test_cert_eu_listing_fails_closed_without_valid_advisories() -> None:
    with pytest.raises(CERTEUAdapterError, match="no bounded advisory links"):
        parse_cert_eu_listing(b"<html><body>No advisories</body></html>", expected_year="2026")


def test_cert_eu_document_normalizes_json_and_retains_raw_provenance() -> None:
    payload = {
        "serial_number": "2026-009",
        "title": "Critical Vulnerabilities in Microsoft SharePoint",
        "publish_date": "23-07-2026 07:13:03",
        "description": "<p>Critical SharePoint vulnerabilities.</p>",
        "content_markdown": "# Summary\nCritical SharePoint vulnerabilities.",
    }
    record = parse_cert_eu_document(
        payload,
        reliability="authoritative",
        document_url="https://cert.europa.eu/publications/security-advisories/2026-009/json",
    )
    assert record.external_id == "CERT-EU-SA-2026-009"
    assert record.object_type == "security-advisory"
    assert record.url.endswith("/2026-009")
    assert record.summary == "Critical SharePoint vulnerabilities."
    assert record.source_reliability == "authoritative"
    assert record.confidence == 93
    assert record.raw == payload


def test_cert_eu_document_fails_closed_on_identity_url_mismatch() -> None:
    payload = {
        "serial_number": "2026-009",
        "title": "Example",
        "publish_date": "23-07-2026 07:13:03",
    }
    with pytest.raises(CERTEUAdapterError, match="does not match"):
        parse_cert_eu_document(
            payload,
            reliability="authoritative",
            document_url="https://cert.europa.eu/publications/security-advisories/2026-008/json",
        )
