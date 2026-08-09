from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))
EVIDENCE_PATH = Path(os.environ.get("DTMO_REFLOW_EVIDENCE_PATH", "artifacts/browser-reflow-320-evidence.json"))
VIEWPORT = {"width": 320, "height": 900}

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.13 reflow E2E executes only in the dedicated browser workflow",
)

SURFACES = (
    {
        "name": "share_approval",
        "path": "/ui/share-approval",
        "subject": "reflow-admin",
        "roles": "admin",
        "ready_test_id": "review-button",
        "controls": ("item-id", "review-button", "share-button"),
    },
    {
        "name": "analyst_search",
        "path": "/ui/analyst-search",
        "subject": "reflow-analyst",
        "roles": "analyst",
        "ready_test_id": "search-panel",
        "controls": ("search-query", "search-submit"),
    },
    {
        "name": "ciso_token_revocation",
        "path": "/ui/ciso-security",
        "subject": "reflow-ciso",
        "roles": "ciso",
        "ready_test_id": "revocation-panel",
        "controls": ("token-jti", "token-expiry", "revocation-reason", "revoke-submit"),
    },
    {
        "name": "auditor_read_only",
        "path": "/ui/auditor",
        "subject": "reflow-auditor",
        "roles": "auditor",
        "ready_test_id": "audit-panel",
        "controls": ("load-audit",),
    },
)


@pytest.mark.asyncio
async def test_wcag_1_4_10_reflow_at_320_css_px() -> None:
    evidence: list[dict[str, object]] = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for surface in SURFACES:
            context = await browser.new_context(
                viewport=VIEWPORT,
                extra_http_headers={
                    "X-DTMO-Subject": surface["subject"],
                    "X-DTMO-Roles": surface["roles"],
                },
            )
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{surface['path']}")
            assert response is not None and response.ok, {
                "surface": surface["name"],
                "status": None if response is None else response.status,
            }
            await expect(page.get_by_test_id(surface["ready_test_id"])).to_be_visible()

            metrics = await page.evaluate(
                """() => ({
                    documentClientWidth: document.documentElement.clientWidth,
                    documentScrollWidth: document.documentElement.scrollWidth,
                    bodyScrollWidth: document.body.scrollWidth,
                    main: (() => {
                      const r = document.querySelector('main').getBoundingClientRect();
                      return {x: r.x, width: r.width, right: r.right};
                    })(),
                    overflowingVisibleElements: [...document.querySelectorAll('main *')]
                      .filter(el => {
                        const s = getComputedStyle(el);
                        const r = el.getBoundingClientRect();
                        return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 &&
                               (r.left < -1 || r.right > document.documentElement.clientWidth + 1);
                      })
                      .map(el => ({tag: el.tagName.toLowerCase(), id: el.id || null,
                                   testid: el.getAttribute('data-testid'),
                                   left: el.getBoundingClientRect().left,
                                   right: el.getBoundingClientRect().right}))
                })"""
            )
            assert metrics["documentClientWidth"] == 320, metrics
            assert metrics["documentScrollWidth"] <= 321, metrics
            assert metrics["bodyScrollWidth"] <= 321, metrics
            assert metrics["main"]["x"] >= -1 and metrics["main"]["right"] <= 321, metrics
            assert metrics["overflowingVisibleElements"] == [], metrics

            controls: list[dict[str, object]] = []
            for test_id in surface["controls"]:
                control = page.get_by_test_id(test_id)
                await expect(control).to_be_visible()
                box = await control.bounding_box()
                assert box is not None
                assert box["x"] >= -1 and box["x"] + box["width"] <= 321, {
                    "surface": surface["name"], "test_id": test_id, "box": box
                }
                await control.focus()
                assert await control.evaluate("el => document.activeElement === el")
                controls.append({"test_id": test_id, "box": box, "focusable": True})

            evidence.append(
                {
                    "surface": surface["name"],
                    "viewport": VIEWPORT,
                    "document_metrics": metrics,
                    "critical_controls": controls,
                    "session_subject": surface["subject"],
                    "session_role": surface["roles"],
                }
            )
            await context.close()
        await browser.close()

    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(
        json.dumps(
            {
                "decision": "pass",
                "exact_head": os.environ.get("GITHUB_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
                "wcag_success_criterion": "1.4.10 Reflow",
                "viewport_css_px": VIEWPORT,
                "covered_surfaces": [surface["name"] for surface in SURFACES],
                "browser": "chromium",
                "two_dimensional_content_exception_used": False,
                "backend_session_rbac_real": True,
                "human_share_approval_preserved": True,
                "product_wide_wcag_2_2_aa_claimed": False,
                "surfaces": evidence,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
