from __future__ import annotations

import os
from uuid import UUID, uuid4

import httpx
import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
E2E_ENABLED = bool(BASE_URL)

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Exposure functional recovery executes only in the dedicated exact-head same-origin workflow",
)


def _cve_id() -> str:
    return f"CVE-2099-{1_000_000 + (uuid4().int % 9_000_000)}"


async def _ingest_vulnerability(
    *,
    cve_id: str,
    cvss: float,
    epss: float,
    kev: bool,
    vendor: str,
    product: str,
    cwe: str,
) -> str:
    payload = {
        "source_id": "opencve",
        "external_id": cve_id,
        "item_type": "vulnerability",
        "title": f"Functional recovery vulnerability {cve_id}",
        "summary": "Repository-controlled vulnerability evidence for exact-head functional browser acceptance.",
        "canonical_url": f"https://example.invalid/advisories/{cve_id}",
        "severity": "critical" if cvss >= 9 else "medium",
        "confidence": 95,
        "education_relevance": 90,
        "tags": ["functional-recovery", "vulnerability"],
        "provenance": [
            {
                "source_url": f"https://example.invalid/advisories/{cve_id}",
                "publisher": "functional-recovery",
                "confidence": 95,
            }
        ],
        "raw_payload": {
            "_dtmo_vulnerability": {
                "cve_id": cve_id,
                "title": f"Functional recovery vulnerability {cve_id}",
                "description": "Repository-controlled raw vulnerability evidence.",
                "cvss_v31": cvss,
                "epss": epss,
                "kev": kev,
                "vendors": [vendor],
                "products": [product],
                "cwes": [cwe],
            }
        },
    }
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers={
            "X-DTMO-Subject": "functional-recovery-exposure-analyst",
            "X-DTMO-Roles": "admin",
        },
        timeout=30,
    ) as client:
        response = await client.post("/api/v1/intelligence", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["share_approved"] is False
    assert body["raw_sha256"]
    return str(body["id"])


async def _cleanup(item_ids: list[str]) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(
            delete(IntelligenceItem).where(IntelligenceItem.id.in_([UUID(item_id) for item_id in item_ids]))
        )
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_exposure_reads_verified_raw_evidence_and_filters_real_projection() -> None:
    """Prove the canonical Exposure read/filter/provenance journey without mocks.

    The fixtures are ingested through the real DTMO API, which persists canonical
    PostgreSQL state and immutable raw evidence in the configured object store.
    This remains repository-controlled evidence only and does not prove local
    asset exposure, exploitability, compromise, remediation or production readiness.
    """
    target_cve = _cve_id()
    decoy_cve = _cve_id()
    while decoy_cve == target_cve:
        decoy_cve = _cve_id()
    suffix = uuid4().hex[:8]
    target_vendor = f"RecoveryVendor-{suffix}"
    target_product = f"RecoveryProduct-{suffix}"
    item_ids: list[str] = []

    try:
        item_ids.append(
            await _ingest_vulnerability(
                cve_id=target_cve,
                cvss=9.8,
                epss=0.72,
                kev=True,
                vendor=target_vendor,
                product=target_product,
                cwe="CWE-79",
            )
        )
        item_ids.append(
            await _ingest_vulnerability(
                cve_id=decoy_cve,
                cvss=6.4,
                epss=0.05,
                kev=False,
                vendor=f"OtherVendor-{suffix}",
                product=f"OtherProduct-{suffix}",
                cwe="CWE-200",
            )
        )

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-exposure-reader",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()
            await page.goto(f"{BASE_URL}/workbench/exposure")

            await expect(page.get_by_role("heading", name="Vulnerability & Exposure Center", exact=True)).to_be_visible()
            await expect(page.get_by_text(target_cve, exact=True)).to_be_visible()
            await expect(page.get_by_text(decoy_cve, exact=True)).to_be_visible()

            target_row = page.get_by_role("listitem").filter(has_text=target_cve)
            await expect(target_row).to_contain_text("opencve · CVSS 9.8 · EPSS 0.72 · CISA KEV evidence present")
            await expect(target_row.get_by_text("raw evidence bound", exact=True)).to_be_visible()
            await expect(target_row.get_by_role("link", name="Open evidence source")).to_have_attribute(
                "href", f"https://example.invalid/advisories/{target_cve}"
            )

            await page.get_by_label("Priority view").select_option("kev")
            await page.get_by_label("Vendor").fill(target_vendor)
            await page.get_by_label("Product").fill(target_product)
            await page.get_by_label("CWE").fill("CWE-79")
            await page.get_by_label("Minimum EPSS (%)").fill("70")

            await expect(page.get_by_text("1 matching", exact=True)).to_be_visible()
            await expect(page.get_by_text(target_cve, exact=True)).to_be_visible()
            await expect(page.get_by_text(decoy_cve, exact=True)).to_have_count(0)
            await expect(page.get_by_text("Prioritize vulnerabilities without inventing local exposure", exact=True)).to_be_visible()
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_ids)
