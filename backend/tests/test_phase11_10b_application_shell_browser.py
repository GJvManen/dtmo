from __future__ import annotations

import os

import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.getenv("DTMO_BROWSER_BASE_URL", "http://127.0.0.1:8000")


@pytest.mark.browser
def test_canonical_workbench_shell_navigation_and_context(page: Page) -> None:
    page.goto(f"{BASE_URL}/")
    page.wait_for_url("**/workbench/command-center")
    expect(page.get_by_role("heading", name="Command Center", level=1)).to_be_visible()
    expect(page.get_by_role("navigation", name="Werkruimten")).to_be_visible()
    expect(page.get_by_text("Geen object geselecteerd")).to_be_visible()
    expect(page.get_by_text("No synthetic operational state")).to_be_visible()
    expect(page.get_by_role("link", name="Compatibility console")).to_be_visible()

    page.keyboard.press("Control+k")
    expect(page.get_by_role("dialog", name="Command palette")).to_be_visible()
    page.get_by_label("Zoek werkruimte").fill("Threat Intelligence")
    page.get_by_role("dialog", name="Command palette").get_by_role("button", name="Threat Intelligence Intelligence").click()
    page.wait_for_url("**/workbench/intelligence")
    expect(page.get_by_role("heading", name="Threat Intelligence", level=1)).to_be_visible()


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
