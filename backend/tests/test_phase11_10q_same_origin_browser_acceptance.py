from __future__ import annotations

import os
from uuid import uuid4

import pytest
from playwright.async_api import ConsoleMessage, Response, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
E2E_ENABLED = bool(BASE_URL)

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Phase 11.10q same-origin browser acceptance executes only in its dedicated exact-head workflow",
)


@pytest.mark.asyncio
async def test_canonical_workbench_uses_real_same_origin_api_and_persistence() -> None:
    """Exercise the built workbench without Playwright API interception.

    This is repository-controlled acceptance against the exact-head DTMO process and
    its temporary persistence only. It deliberately does not call an external source,
    and it is not live/staging/production-equivalent or external-assurance evidence.
    """

    page_errors: list[str] = []
    console_errors: list[str] = []
    server_errors: list[str] = []
    api_responses: list[str] = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "phase11-10q-same-origin-acceptance",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()
        page.on("pageerror", lambda error: page_errors.append(str(error)))

        def capture_console(message: ConsoleMessage) -> None:
            if message.type == "error":
                console_errors.append(message.text)

        def capture_response(response: Response) -> None:
            if response.url.startswith(f"{BASE_URL}/api/v1/"):
                api_responses.append(f"{response.status} {response.url}")
                if response.status >= 500:
                    server_errors.append(f"{response.status} {response.url}")

        page.on("console", capture_console)
        page.on("response", capture_response)

        # The browser must talk to the real same-origin session and command-center API.
        await page.goto(f"{BASE_URL}/workbench/command-center")
        await expect(page.get_by_role("heading", name="Command Center", exact=True)).to_be_visible()
        session_response = await context.request.get(f"{BASE_URL}/api/v1/ui/session")
        assert session_response.status == 200
        session = await session_response.json()
        assert session["subject"] == "phase11-10q-same-origin-acceptance"
        assert "manage:connectors" in session["permissions"]

        command_response = await context.request.get(f"{BASE_URL}/api/v1/command-center")
        assert command_response.status == 200
        command = await command_response.json()
        assert command["data_state"] in {"available", "unavailable"}
        assert "evidence_boundary" in command

        # Prove a real browser mutation reaches DTMO persistence. The source is created
        # disabled and points at .invalid, so this journey never performs an external fetch.
        await page.goto(f"{BASE_URL}/workbench/collection")
        await expect(page.get_by_role("heading", name="Sources & Collection", exact=True)).to_be_visible()
        await expect(page.get_by_role("button", name="Register source", exact=True)).to_be_enabled()

        source_id = f"acceptance-local-{uuid4().hex[:12]}"
        await page.get_by_role("button", name="Register source", exact=True).click()
        registration = page.get_by_role("form", name="Register source")
        await registration.get_by_label("Source ID").fill(source_id)
        await registration.get_by_label("Name").fill("Repository-controlled same-origin acceptance source")
        await registration.get_by_label("HTTPS endpoint").fill("https://example.invalid/dtmo-same-origin-acceptance.json")
        await registration.get_by_label("Interval seconds").fill("3600")
        await registration.get_by_label("Reliability").select_option("medium")
        async with page.expect_response(
            lambda response: response.url == f"{BASE_URL}/api/v1/admin/sources"
            and response.request.method == "POST"
        ) as registration_response_info:
            await registration.get_by_role("button", name="Register disabled source", exact=True).click()
        registration_response = await registration_response_info.value
        assert registration_response.status == 201

        sources_response = await context.request.get(f"{BASE_URL}/api/v1/admin/sources")
        assert sources_response.status == 200
        sources = await sources_response.json()
        persisted = next((source for source in sources if source["id"] == source_id), None)
        assert persisted is not None
        assert persisted["enabled"] is False
        assert persisted["endpoint_url"] == "https://example.invalid/dtmo-same-origin-acceptance.json"

        # Reloading the workspace must read the persisted source back through the same-origin API.
        await page.reload()
        await expect(page.get_by_role("heading", name="Sources & Collection", exact=True)).to_be_visible()
        await expect(page.get_by_text("Repository-controlled same-origin acceptance source", exact=True)).to_be_visible()

        # Exercise every recovered canonical surface against the actual DTMO process.
        journeys = (
            ("/workbench/intelligence", "Threat Intelligence"),
            ("/workbench/intelligence/iocs", "IOC Explorer"),
            ("/workbench/intelligence/graph", "Knowledge Graph"),
            ("/workbench/exposure", "Vulnerability & Exposure Center"),
            ("/workbench/analysis", "Analysis & Enrichment"),
            ("/workbench/sharing", "Sharing & Exchange"),
            ("/workbench/automation", "Automation & Playbooks"),
            ("/workbench/governance", "Governance & Evidence"),
            ("/workbench/administration", "Administration"),
            ("/workbench/command-center", "Command Center"),
        )
        for path, heading in journeys:
            await page.goto(f"{BASE_URL}{path}")
            await expect(page.get_by_role("heading", name=heading, exact=True)).to_be_visible()

        # Critical proof: no route interception was installed; calls above are actual HTTP
        # responses from the exact-head DTMO process. Require a meaningful API sample and
        # fail closed on browser/runtime server errors.
        assert len(api_responses) >= 10, api_responses
        assert server_errors == [], server_errors
        assert page_errors == [], page_errors
        assert console_errors == [], console_errors

        await context.close()
        await browser.close()
