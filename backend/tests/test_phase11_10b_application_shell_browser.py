from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, expect, sync_playwright

BASE_URL = os.getenv("DTMO_BROWSER_BASE_URL", "").rstrip("/")


@pytest.fixture()
def page() -> Iterator[Page]:
    """Run only in the dedicated browser environment with installed Chromium."""
    if not BASE_URL:
        pytest.skip("Phase 11.10b browser acceptance requires DTMO_BROWSER_BASE_URL")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


@pytest.mark.browser
def test_canonical_workbench_shell_navigation_and_context(page: Page) -> None:
    page.goto(f"{BASE_URL}/")
    page.wait_for_url("**/workbench/command-center")
    expect(page.get_by_role("heading", name="Command Center", level=1)).to_be_visible()
    expect(page.get_by_role("navigation", name="Werkruimten")).to_be_visible()
    expect(page.get_by_text("Geen object geselecteerd")).to_be_visible()
    expect(page.get_by_role("heading", name="Operational visibility without synthetic claims", level=2)).to_be_visible()
    expect(page.get_by_role("link", name="Compatibility console", exact=True)).to_be_visible()

    page.keyboard.press("Control+k")
    palette = page.get_by_role("dialog", name="Command palette")
    expect(palette).to_be_visible()
    page.get_by_label("Zoek werkruimte").fill("Threat Intelligence")
    palette.get_by_role("button").filter(has_text="Threat Intelligence").click()
    page.wait_for_url("**/workbench/intelligence")
    expect(page.get_by_role("heading", name="Threat Intelligence", level=1)).to_be_visible()
    expect(page.get_by_text("Recent intelligence is read from canonical DTMO persistence", exact=False)).to_be_visible()
    expect(page.get_by_role("heading", name="Canonical recent view without fabricated content", level=2)).to_be_visible()

    page.get_by_role("link", name="Operations").click()
    page.wait_for_url("**/workbench/operations")
    expect(page.get_by_role("heading", name="Operations", level=1)).to_be_visible()
    expect(page.get_by_role("heading", name="Operational snapshot", level=2)).to_be_visible()
    expect(page.get_by_text("Missing telemetry stays unavailable", exact=False)).to_be_visible()
    expect(page.get_by_role("heading", name="Act without legacy fallback", level=2)).to_be_visible()


@pytest.mark.browser
def test_shell_has_keyboard_skip_link_and_mobile_navigation(page: Page) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{BASE_URL}/workbench/command-center")
    expect(page.get_by_role("link", name="Ga naar hoofdinhoud")).to_have_attribute("href", "#main-workspace")
    menu = page.get_by_role("button", name="Navigatie openen")
    expect(menu).to_be_visible()
    menu.click()
    expect(page.get_by_role("navigation", name="Werkruimten")).to_be_visible()
    page.get_by_role("link", name="Operations").click()
    page.wait_for_url("**/workbench/operations")
    expect(page.get_by_role("heading", name="Operations", level=1)).to_be_visible()
