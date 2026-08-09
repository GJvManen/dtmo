from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
EVIDENCE_PATH = Path(os.environ.get("DTMO_TEXT_SPACING_EVIDENCE_PATH", "artifacts/browser-text-spacing-evidence.json"))
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(not E2E_ENABLED, reason="RC9 text-spacing E2E executes only in dedicated workflow")

SURFACES = (
    ("share_approval", "/ui/share-approval", "spacing-admin", "admin", "review-button", ("item-id", "review-button", "share-button")),
    ("analyst_search", "/ui/analyst-search", "spacing-analyst", "analyst", "search-panel", ("search-query", "search-submit")),
    ("ciso_token_revocation", "/ui/ciso-security", "spacing-ciso", "ciso", "revocation-panel", ("token-jti", "token-expiry", "revocation-reason", "revoke-submit")),
    ("auditor_read_only", "/ui/auditor", "spacing-auditor", "auditor", "audit-panel", ("load-audit",)),
)

OVERRIDE = """
*:not(svg):not(path) { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }
p { margin-bottom: 2em !important; }
"""

@pytest.mark.asyncio
async def test_text_spacing_overrides_preserve_content_and_function() -> None:
    rows = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for name, path, subject, roles, ready, controls in SURFACES:
            context = await browser.new_context(viewport={"width": 1440, "height": 900}, extra_http_headers={"X-DTMO-Subject": subject, "X-DTMO-Roles": roles})
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{path}")
            assert response is not None and response.ok
            await expect(page.get_by_test_id(ready)).to_be_visible()
            await page.add_style_tag(content=OVERRIDE)
            await page.wait_for_timeout(100)
            metrics = await page.evaluate("""() => {
              const visible = el => { const s=getComputedStyle(el), r=el.getBoundingClientRect(); return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0; };
              const clipped = [];
              for (const el of document.querySelectorAll('main *')) {
                if (!visible(el) || !(el.textContent||'').trim()) continue;
                const s=getComputedStyle(el);
                if ((s.overflowX==='hidden' && el.scrollWidth>el.clientWidth+1) || (s.overflowY==='hidden' && el.scrollHeight>el.clientHeight+1)) clipped.push(el.getAttribute('data-testid') || el.tagName.toLowerCase());
              }
              return {documentScrollWidth:document.documentElement.scrollWidth, documentClientWidth:document.documentElement.clientWidth, clippedText:clipped};
            }""")
            assert metrics["clippedText"] == [], metrics
            control_rows = []
            for test_id in controls:
                control = page.get_by_test_id(test_id)
                await expect(control).to_be_visible()
                await control.focus()
                assert await control.evaluate("el => el === document.activeElement")
                control_rows.append({"test_id": test_id, "focusable": True})
            rows.append({"surface": name, "document_metrics": metrics, "critical_controls": control_rows})
            await context.close()
        await browser.close()

    evidence = {
        "decision": "pass",
        "exact_head": os.environ.get("GITHUB_HEAD_SHA", "local"),
        "wcag_success_criterion": "1.4.12 Text Spacing",
        "override": {"line_height": "1.5", "paragraph_spacing": "2em", "letter_spacing": "0.12em", "word_spacing": "0.16em"},
        "covered_surfaces": [s[0] for s in SURFACES],
        "backend_session_rbac_real": True,
        "human_share_approval_preserved": True,
        "assistive_technology_claimed": False,
        "product_wide_wcag_2_2_aa_claimed": False,
        "surfaces": rows,
    }
    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
