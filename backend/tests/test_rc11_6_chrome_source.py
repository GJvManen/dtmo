from __future__ import annotations

from dtmo.chrome_adapter import (
    CHROME_EXECUTION_PROFILE,
    discover_chrome_stable_posts,
    parse_chrome_security_post,
)
from dtmo.source_catalog import catalog_by_id
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY


def test_chrome_catalog_source_is_supported_and_registered() -> None:
    source = catalog_by_id("google-chrome-releases")
    assert source is not None
    assert source.execution_status == "supported"
    assert source.execution_profile == CHROME_EXECUTION_PROFILE
    assert source.endpoint_url == "https://chromereleases.googleblog.com/"
    assert SOURCE_ADAPTER_REGISTRY.get(CHROME_EXECUTION_PROFILE) is not None


def test_discovery_accepts_only_first_party_stable_posts_and_deduplicates() -> None:
    payload = b"""
    <a href="https://chromereleases.googleblog.com/2026/04/stable-channel-update-for-desktop.html">Stable Channel Update for Desktop</a>
    <a href="/2026/04/stable-channel-update-for-desktop.html">Stable Channel Update for Desktop</a>
    <a href="https://chromereleases.googleblog.com/2026/04/dev-channel-update.html">Chrome Dev for Desktop Update</a>
    <a href="https://example.org/2026/04/stable-channel-update.html">Stable Channel Update</a>
    """
    posts = discover_chrome_stable_posts(payload)
    assert posts == [
        (
            "stable-channel-update-for-desktop",
            "https://chromereleases.googleblog.com/2026/04/stable-channel-update-for-desktop.html",
            "Stable Channel Update for Desktop",
        )
    ]


def test_security_post_requires_security_section_and_published_cve() -> None:
    record = parse_chrome_security_post(
        b"<html><body><h3>Security Fixes and Rewards</h3><p>High CVE-2026-5858: test</p></body></html>",
        slug="stable-channel-update-for-desktop",
        url="https://chromereleases.googleblog.com/2026/04/stable-channel-update-for-desktop.html",
        title="Stable Channel Update for Desktop",
        reliability="authoritative",
    )
    assert record is not None
    assert record.external_id == "CHROME-stable-channel-update-for-desktop"
    assert record.raw["cves"] == ["CVE-2026-5858"]
    assert record.source_reliability == "authoritative"


def test_non_security_stable_post_is_not_ingested() -> None:
    record = parse_chrome_security_post(
        b"<html><body><p>Stable update with general fixes only.</p></body></html>",
        slug="stable-channel-update",
        url="https://chromereleases.googleblog.com/2026/06/stable-channel-update.html",
        title="Stable Channel Update",
        reliability="authoritative",
    )
    assert record is None
