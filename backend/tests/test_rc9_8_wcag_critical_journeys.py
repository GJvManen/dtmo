from __future__ import annotations

import os

import pytest
from playwright.async_api import Page, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.8 accessibility E2E executes only in the dedicated browser workflow",
)

SURFACES = (
    ("share_approval", "/ui/share-approval", "wcag-admin", "admin", "review-button"),
    ("analyst_search", "/ui/analyst-search", "wcag-analyst", "analyst", "search-submit"),
    ("ciso_token_revocation", "/ui/ciso-security", "wcag-ciso", "ciso", "revoke-submit"),
    ("auditor_read_only", "/ui/auditor", "wcag-auditor", "auditor", "load-audit"),
)


async def _assert_accessible_document(page: Page) -> None:
    lang = await page.locator("html").get_attribute("lang")
    assert lang and lang.strip(), "WCAG 3.1.1: html language must be declared"
    assert (await page.title()).strip(), "WCAG 2.4.2: document title must be non-empty"
    await expect(page.locator("main")).to_have_count(1)
    assert await page.locator("h1, h2, h3, h4, h5, h6").count() >= 1, "WCAG 1.3.1: heading structure missing"

    duplicate_ids = await page.evaluate(
        """() => {
          const ids = [...document.querySelectorAll('[id]')].map(el => el.id).filter(Boolean);
          return [...new Set(ids.filter((id, idx) => ids.indexOf(id) !== idx))];
        }"""
    )
    assert duplicate_ids == [], f"WCAG 4.1.1 compatibility: duplicate ids: {duplicate_ids}"

    missing_alt = await page.evaluate(
        """() => [...document.querySelectorAll('img')]
          .filter(img => !img.hasAttribute('alt'))
          .map(img => img.getAttribute('src') || '<inline>')"""
    )
    assert missing_alt == [], f"WCAG 1.1.1: images without alt attribute: {missing_alt}"

    unnamed_controls = await page.evaluate(
        """() => {
          const controls = [...document.querySelectorAll('button, input, select, textarea, a[href]')];
          const name = el => {
            const aria = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby');
            if (aria && aria.trim()) return aria.trim();
            if (el.id) {
              const label = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
              if (label && label.textContent.trim()) return label.textContent.trim();
            }
            if (el.closest('label')?.textContent?.trim()) return el.closest('label').textContent.trim();
            if (el.getAttribute('title')?.trim()) return el.getAttribute('title').trim();
            if (el.textContent?.trim()) return el.textContent.trim();
            if (el.getAttribute('value')?.trim()) return el.getAttribute('value').trim();
            return '';
          };
          return controls.filter(el => !name(el)).map(el => el.outerHTML.slice(0, 180));
        }"""
    )
    assert unnamed_controls == [], f"WCAG 4.1.2/3.3.2: unnamed controls: {unnamed_controls}"


async def _assert_keyboard_focus(page: Page, ready_test_id: str) -> None:
    target = page.get_by_test_id(ready_test_id)
    await expect(target).to_be_visible()
    for _ in range(20):
        await page.keyboard.press("Tab")
        if await target.evaluate("el => el === document.activeElement"):
            focus = await target.evaluate(
                """el => {
                  const s = getComputedStyle(el);
                  return {outlineStyle:s.outlineStyle, outlineWidth:s.outlineWidth, boxShadow:s.boxShadow};
                }"""
            )
            has_outline = focus["outlineStyle"] != "none" and focus["outlineWidth"] not in {"0", "0px"}
            has_shadow = focus["boxShadow"] not in {"none", ""}
            assert has_outline or has_shadow, f"WCAG 2.4.7/2.4.11: no visible focus: {focus}"
            return
    raise AssertionError(f"WCAG 2.1.1: keyboard focus never reached {ready_test_id}")


@pytest.mark.asyncio
async def test_applicable_wcag_2_2_aa_controls_on_critical_journeys() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for name, path, subject, roles, ready_test_id in SURFACES:
            context = await browser.new_context(
                extra_http_headers={"X-DTMO-Subject": subject, "X-DTMO-Roles": roles}
            )
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{path}")
            assert response is not None and response.ok, {"surface": name, "status": None if response is None else response.status}
            await _assert_accessible_document(page)
            await _assert_keyboard_focus(page, ready_test_id)
            await context.close()
        await browser.close()
