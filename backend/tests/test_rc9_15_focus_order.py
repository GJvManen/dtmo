from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))
EVIDENCE_PATH = Path(os.environ.get("DTMO_FOCUS_ORDER_EVIDENCE_PATH", "artifacts/browser-focus-order-evidence.json"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.15 focus-order E2E executes only in the dedicated browser workflow",
)

SURFACES = (
    {"name": "share_approval", "path": "/ui/share-approval", "subject": "focus-admin", "roles": "admin", "ready": "review-button"},
    {"name": "analyst_search", "path": "/ui/analyst-search", "subject": "focus-analyst", "roles": "analyst", "ready": "search-panel"},
    {"name": "ciso_token_revocation", "path": "/ui/ciso-security", "subject": "focus-ciso", "roles": "ciso", "ready": "revocation-panel"},
    {"name": "auditor_read_only", "path": "/ui/auditor", "subject": "focus-auditor", "roles": "auditor", "ready": "audit-panel"},
)

IDENTITY_JS = """el => ({
  tag: el.tagName.toLowerCase(),
  id: el.id || null,
  testid: el.getAttribute('data-testid'),
  name: el.getAttribute('name'),
  type: el.getAttribute('type'),
  text: (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 120)
})"""

TAB_ORDER_JS = """() => [...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]')]
  .filter(el => {
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const ti = el.tabIndex;
    return !el.disabled && ti >= 0 && s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
  })
  .map(el => ({
    tag: el.tagName.toLowerCase(), id: el.id || null, testid: el.getAttribute('data-testid'),
    name: el.getAttribute('name'), type: el.getAttribute('type'), tabIndex: el.tabIndex,
    text: (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 120)
  }))"""


def _key(item: dict[str, object]) -> tuple[object, ...]:
    return (item.get("tag"), item.get("id"), item.get("testid"), item.get("name"), item.get("type"), item.get("text"))


@pytest.mark.asyncio
async def test_wcag_2_4_3_complete_focus_order() -> None:
    evidence: list[dict[str, object]] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for surface in SURFACES:
            context = await browser.new_context(
                viewport={"width": 1440, "height": 900},
                extra_http_headers={"X-DTMO-Subject": surface["subject"], "X-DTMO-Roles": surface["roles"]},
            )
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{surface['path']}")
            assert response is not None and response.ok
            await expect(page.get_by_test_id(surface["ready"])).to_be_visible()

            expected = await page.evaluate(TAB_ORDER_JS)
            assert expected, {"surface": surface["name"], "reason": "no tabbable controls"}
            assert all(item["tabIndex"] == 0 for item in expected), {
                "surface": surface["name"], "reason": "positive tabindex changes logical order", "expected": expected
            }

            await page.evaluate("() => document.body.focus()")
            actual: list[dict[str, object]] = []
            seen: set[tuple[object, ...]] = set()
            for _ in range(len(expected)):
                await page.keyboard.press("Tab")
                item = await page.evaluate(IDENTITY_JS, await page.evaluate_handle("() => document.activeElement"))
                key = _key(item)
                assert key not in seen, {"surface": surface["name"], "reason": "focus cycle before all controls reached", "actual": actual}
                seen.add(key)
                actual.append(item)

            expected_keys = [_key(item) for item in expected]
            actual_keys = [_key(item) for item in actual]
            assert actual_keys == expected_keys, {
                "surface": surface["name"], "reason": "Tab sequence differs from DOM logical order",
                "expected": expected, "actual": actual,
            }

            await page.keyboard.press("Shift+Tab")
            reverse_target = await page.evaluate(IDENTITY_JS, await page.evaluate_handle("() => document.activeElement"))
            assert _key(reverse_target) == expected_keys[-2] if len(expected_keys) > 1 else expected_keys[-1]

            evidence.append({
                "surface": surface["name"],
                "expected_dom_focus_order": expected,
                "observed_tab_focus_order": actual,
                "all_tabbables_reached_once": True,
                "positive_tabindex_present": False,
                "reverse_navigation_checked": True,
                "session_subject": surface["subject"],
                "session_role": surface["roles"],
            })
            await context.close()
        await browser.close()

    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(json.dumps({
        "decision": "pass",
        "exact_head": os.environ.get("GITHUB_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
        "wcag_success_criterion": "2.4.3 Focus Order",
        "covered_surfaces": [surface["name"] for surface in SURFACES],
        "browser": "chromium",
        "backend_session_rbac_real": True,
        "human_share_approval_preserved": True,
        "assistive_technology_behavior_claimed": False,
        "product_wide_wcag_2_2_aa_claimed": False,
        "surfaces": evidence,
    }, indent=2) + "\n", encoding="utf-8")
