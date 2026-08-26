from __future__ import annotations

import os

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
E2E_ENABLED = bool(BASE_URL)

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Owner functional recovery browser matrix executes only in the dedicated exact-head same-origin workflow",
)


@pytest.mark.asyncio
async def test_all_canonical_routes_render_and_administration_persists_changes() -> None:
    """Exercise every canonical route and one real Administration mutation.

    This is repository-controlled exact-head evidence against the real DTMO process and
    temporary persistence. It does not execute external connectors and is not owner,
    staging, production-equivalent, production, pentest, or independent-assurance evidence.
    """
    routes = (
        ("/workbench/command-center", "Command Center"),
        ("/workbench/intelligence", "Threat Intelligence"),
        ("/workbench/intelligence/iocs", "IOC Explorer"),
        ("/workbench/intelligence/graph", "Knowledge Graph"),
        ("/workbench/exposure", "Vulnerability & Exposure Center"),
        ("/workbench/investigations", "Investigations"),
        ("/workbench/analysis", "Analysis & Enrichment"),
        ("/workbench/sharing", "Sharing & Exchange"),
        ("/workbench/automation", "Automation & Playbooks"),
        ("/workbench/collection", "Sources & Collection"),
        ("/workbench/governance", "Governance & Evidence"),
        ("/workbench/operations", "Operations"),
        ("/workbench/administration", "Administration"),
    )

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "owner-functional-recovery-matrix",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()

        for path, heading in routes:
            await page.goto(f"{BASE_URL}{path}")
            await expect(page.get_by_role("heading", name=heading, exact=True)).to_be_visible()
            assert await page.locator('a[href^="/ui/"]').count() == 0

        await page.goto(f"{BASE_URL}/workbench/administration")
        await expect(page.get_by_role("heading", name="Administration", exact=True)).to_be_visible()
        await expect(page.get_by_text("Runtime configuration", exact=True)).to_be_visible()

        integration_cards = page.locator("[data-integration]")
        assert await integration_cards.count() >= 7

        misp = page.locator('[data-integration="misp"]')
        endpoint = misp.get_by_label("API endpoint")
        enabled = misp.get_by_label("Enabled")
        save = misp.get_by_role("button", name="Save configuration", exact=True)

        original_endpoint = await endpoint.input_value()
        original_enabled = await enabled.is_checked()
        acceptance_endpoint = "https://example.invalid/dtmo-functional-acceptance-misp"

        await endpoint.fill(acceptance_endpoint)
        if await enabled.is_checked():
            await enabled.uncheck()
        await expect(save).to_be_enabled()

        async with page.expect_response(
            lambda response: response.url == f"{BASE_URL}/api/v1/admin/integrations/misp"
            and response.request.method == "PATCH"
        ) as save_response_info:
            await save.click()
        save_response = await save_response_info.value
        assert save_response.status == 200

        await page.reload()
        await expect(page.get_by_role("heading", name="Administration", exact=True)).to_be_visible()
        misp = page.locator('[data-integration="misp"]')
        endpoint = misp.get_by_label("API endpoint")
        enabled = misp.get_by_label("Enabled")
        save = misp.get_by_role("button", name="Save configuration", exact=True)
        await expect(endpoint).to_have_value(acceptance_endpoint)
        assert await enabled.is_checked() is False

        # Restore the repository-controlled runtime fixture so later assertions are isolated.
        await endpoint.fill(original_endpoint)
        if original_enabled:
            await enabled.check()
        await expect(save).to_be_enabled()
        async with page.expect_response(
            lambda response: response.url == f"{BASE_URL}/api/v1/admin/integrations/misp"
            and response.request.method == "PATCH"
        ) as restore_response_info:
            await save.click()
        restore_response = await restore_response_info.value
        assert restore_response.status == 200

        await page.reload()
        misp = page.locator('[data-integration="misp"]')
        await expect(misp.get_by_label("API endpoint")).to_have_value(original_endpoint)
        assert await misp.get_by_label("Enabled").is_checked() is original_enabled

        await context.close()
        await browser.close()
