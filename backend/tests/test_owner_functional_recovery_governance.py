from __future__ import annotations

import os

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="Governance functional recovery executes only in the dedicated exact-head browser workflow",
)


@pytest.mark.asyncio
async def test_governance_exposes_repository_backed_framework_control_and_provenance_evidence() -> None:
    """Prove a canonical deep framework -> control -> implementation/provenance journey."""
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "functional-recovery-governance-human",
                "X-DTMO-Roles": "auditor",
            }
        )
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/workbench/governance")

        await expect(page.get_by_role("heading", name="Governance & Evidence", exact=True)).to_be_visible()
        frameworks = page.locator('[data-governance-section="frameworks"]')
        await expect(frameworks).to_contain_text("Normenkader IBP")
        await expect(frameworks).to_contain_text("MITRE ATT&CK")
        await expect(frameworks).to_contain_text("NIST Cybersecurity Framework")
        await expect(frameworks).to_contain_text("CVSS")
        await expect(frameworks).to_contain_text("Provenance:")

        crosswalk = page.locator('[data-governance-section="control-crosswalk"]')
        await expect(crosswalk).to_contain_text("explicit mappings")
        tvm = page.locator('[data-governance-control="DTMO-TVM-01"]')
        await expect(tvm).to_contain_text("SM.07")
        await expect(tvm).to_contain_text("T1087")
        await expect(tvm).to_contain_text("CVSS:4.0")
        await expect(tvm).to_contain_text("backend/dtmo/connectors/")
        await expect(tvm).to_contain_text("context-only")

        await expect(page.get_by_text("Mapping visibility ≠ compliance approval", exact=True)).to_be_visible()
        claim_boundary = page.locator("article.evidence-surface").filter(
            has=page.get_by_role("heading", name="Evidence without synthetic assurance", exact=True)
        )
        await expect(claim_boundary).to_contain_text(
            "Visibility does not grant review, case, connector, share, publication, administration or production authority."
        )
        assert await page.locator('a[href^="/ui/"]').count() == 0

        await context.close()
        await browser.close()
