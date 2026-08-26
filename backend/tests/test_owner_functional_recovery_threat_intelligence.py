from __future__ import annotations

import os
from uuid import UUID, uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.intelligence.model import ConfidenceLevel, IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database
from dtmo.search.service import OpenSearchService

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Threat Intelligence functional recovery executes only in the dedicated same-origin browser workflow",
)


async def _seed_intelligence() -> tuple[str, str]:
    database = Database()
    external_id = f"functional-recovery-{uuid4()}"
    item = IntelligenceItem(
        source_id="functional-recovery-browser",
        external_id=external_id,
        item_type=IntelligenceType.ADVISORY,
        title="Functional recovery ransomware advisory",
        summary="Repository-controlled canonical intelligence fixture used to prove the unmocked Threat Intelligence read path.",
        canonical_url="https://example.invalid/functional-recovery-ransomware",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=91,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled exact-head browser acceptance fixture"],
        education_relevance=96,
        review_status="candidate",
        share_approved=False,
        metadata_json={
            "fixture": "repository-controlled-functional-recovery",
            "cve_ids": ["CVE-2026-4242"],
            "known_exploited": True,
            "vendor": "Example Vendor",
            "product": "Example Product",
            "tags": ["ransomware", "education"],
        },
    )
    async for session in database.session():
        session.add(item)
        await session.flush()
        item_id = str(item.id)
        await session.commit()
        break
    await database.close()
    return item_id, external_id


async def _seed_searchable_intelligence() -> tuple[str, str, str]:
    database = Database()
    external_id = f"search-recovery-{uuid4().hex}"
    search_token = external_id
    title = f"Functional recovery searchable advisory {search_token}"
    item = IntelligenceItem(
        source_id="functional-recovery-search",
        external_id=external_id,
        item_type=IntelligenceType.ADVISORY,
        title=title,
        summary="Repository-controlled searchable fixture for the real OpenSearch-backed Threat Intelligence projection.",
        canonical_url=f"https://example.invalid/{external_id}",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=94,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled search projection fixture"],
        education_relevance=97,
        review_status="candidate",
        share_approved=False,
        metadata_json={"fixture": "repository-controlled-search-functional-recovery"},
    )
    async for session in database.session():
        session.add(item)
        await session.flush()
        item_id = str(item.id)
        await session.commit()
        break
    await database.close()

    search = OpenSearchService()
    try:
        await search.index_document(
            item_id,
            {
                "title": title,
                "summary": item.summary,
                "item_type": item.item_type.value,
                "source_id": item.source_id,
                "severity": item.severity.value,
                "confidence_score": item.confidence_score,
                "confidence_level": item.confidence_level.value,
                "confidence_rationale": item.confidence_rationale,
                "education_relevance": item.education_relevance,
                "published_at": None,
                "canonical_url": item.canonical_url,
                "tags": ["search-functional-recovery", search_token],
            },
        )
    finally:
        await search.close()
    return item_id, search_token, title


async def _cleanup(item_id: str, *, remove_search_document: bool = False) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()
    if remove_search_document:
        search = OpenSearchService()
        try:
            await search.client.delete(
                f"{search.base_url}/{search.index_name}/_doc/{item_id}",
                params={"refresh": "wait_for"},
            )
        finally:
            await search.close()


@pytest.mark.asyncio
async def test_threat_intelligence_reads_real_persistence_and_opens_real_detail() -> None:
    """Prove the canonical recent/detail/pivot journey without browser route interception.

    This is repository-controlled exact-head evidence against temporary PostgreSQL
    persistence. It is not live-source, staging, production-equivalent, pentest,
    owner-acceptance or independent-assurance evidence.
    """
    item_id, _ = await _seed_intelligence()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-analyst",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()

            await page.goto(f"{BASE_URL}/workbench/intelligence")
            await expect(page.get_by_role("heading", name="Threat Intelligence", exact=True)).to_be_visible()
            await expect(page.get_by_text("Recent canonical intelligence", exact=True)).to_be_visible()
            await expect(page.get_by_text("Functional recovery ransomware advisory", exact=True).first).to_be_visible()

            await page.get_by_role("button", name="Open Functional recovery ransomware advisory").click()
            await expect(page.get_by_role("heading", name="Functional recovery ransomware advisory", level=3)).to_be_visible()
            await expect(page.get_by_text("functional-recovery-browser", exact=True)).to_be_visible()
            await expect(page.get_by_text("96/100", exact=True)).to_be_visible()
            await expect(page.get_by_text("91/100 · high", exact=True)).to_be_visible()
            await expect(page.get_by_text("candidate", exact=True)).to_be_visible()
            await expect(page.get_by_text("Not approved for sharing", exact=True)).to_be_visible()

            await expect(page.get_by_role("link", name="Analyze & enrich")).to_have_attribute(
                "href", f"/workbench/analysis?item={item_id}"
            )
            await expect(page.get_by_role("link", name="Review & share")).to_have_attribute(
                "href", f"/workbench/sharing?item={item_id}"
            )
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)


@pytest.mark.asyncio
async def test_threat_intelligence_searches_real_projection_with_filters_and_opens_detail() -> None:
    """Prove query, severity and relevance filters against a real OpenSearch projection."""
    item_id, search_token, title = await _seed_searchable_intelligence()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-search-analyst",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()

            await page.goto(f"{BASE_URL}/workbench/intelligence")
            await page.get_by_label("Search canonical intelligence").fill(search_token)
            await page.get_by_label("Severity").select_option("high")
            await page.get_by_label("Minimum education relevance").fill("95")
            await page.get_by_label("Maximum results").fill("10")
            await page.get_by_role("button", name="Search intelligence").click()

            result_button = page.get_by_role("button", name=f"Open {title}")
            await expect(result_button).to_be_visible()
            await expect(page.get_by_text("1 available", exact=True)).to_be_visible()
            await result_button.click()
            await expect(page.get_by_role("heading", name=title, level=3)).to_be_visible()
            await expect(page.get_by_text("functional-recovery-search", exact=True)).to_be_visible()
            await expect(page.get_by_text("97/100", exact=True)).to_be_visible()
            await expect(page.get_by_text("94/100 · high", exact=True)).to_be_visible()
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id, remove_search_document=True)
