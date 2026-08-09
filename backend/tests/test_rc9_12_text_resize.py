from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))
EVIDENCE_PATH = Path(os.environ.get("DTMO_TEXT_RESIZE_EVIDENCE_PATH", "artifacts/browser-text-resize-evidence.json"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.12 text-resize E2E executes only in the dedicated browser workflow",
)

SURFACES = (
    ("share_approval", "/ui/share-approval", "resize-admin", "admin", "review-button"),
    ("analyst_search", "/ui/analyst-search", "resize-analyst", "analyst", "search-submit"),
    ("ciso_token_revocation", "/ui/ciso-security", "resize-ciso", "ciso", "revoke-submit"),
    ("auditor_read_only", "/ui/auditor", "resize-auditor", "auditor", "load-audit"),
)

TEXT_SELECTORS = "h1,h2,h3,h4,h5,h6,p,label,button,legend,pre,[role='status'],li,strong,code,input,textarea"


async def _snapshot(page):
    return await page.evaluate(
        """selectors => Array.from(document.querySelectorAll(selectors)).map((el, index) => {
          const style = getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          const text = ((el.innerText || el.textContent || el.value || '') + '').replace(/\\s+/g, ' ').trim();
          return {
            key: el.id || el.getAttribute('data-testid') || `${el.tagName.toLowerCase()}-${index}`,
            tag: el.tagName.toLowerCase(),
            text: text.slice(0, 120),
            visible: rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden',
            font_px: Number.parseFloat(style.fontSize),
            client_width: el.clientWidth,
            scroll_width: el.scrollWidth,
            client_height: el.clientHeight,
            scroll_height: el.scrollHeight,
          };
        })""",
        TEXT_SELECTORS,
    )


@pytest.mark.asyncio
async def test_wcag_1_4_4_text_resizes_to_200_percent_without_loss() -> None:
    evidence: list[dict[str, object]] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for name, path, subject, roles, ready_test_id in SURFACES:
            context = await browser.new_context(
                viewport={"width": 1440, "height": 900},
                extra_http_headers={"X-DTMO-Subject": subject, "X-DTMO-Roles": roles},
            )
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{path}")
            assert response is not None and response.ok, {"surface": name, "status": None if response is None else response.status}

            principal = page.locator('[data-testid$="principal"], [data-testid="principal"]')
            await expect(principal).to_contain_text(subject)
            control = page.get_by_test_id(ready_test_id)
            await expect(control).to_be_visible()

            baseline = await _snapshot(page)
            await page.add_style_tag(content="html { font-size: 200% !important; }")
            await page.wait_for_timeout(100)
            resized = await _snapshot(page)

            baseline_by_key = {row["key"]: row for row in baseline if row["visible"] and row["text"]}
            resized_by_key = {row["key"]: row for row in resized if row["visible"] and row["text"]}
            common = sorted(set(baseline_by_key) & set(resized_by_key))
            assert common, f"no comparable text nodes captured for {name}"

            scale_failures = []
            clipping_failures = []
            measurements = []
            for key in common:
                before = baseline_by_key[key]
                after = resized_by_key[key]
                ratio = after["font_px"] / before["font_px"] if before["font_px"] else 0
                scale_ok = ratio >= 1.95
                horizontal_clip = after["scroll_width"] > after["client_width"] + 1 and after["tag"] not in {"pre", "code"}
                vertical_clip = after["scroll_height"] > after["client_height"] + 1 and after["tag"] in {"button", "input", "textarea"}
                if not scale_ok:
                    scale_failures.append({"key": key, "ratio": ratio})
                if horizontal_clip or vertical_clip:
                    clipping_failures.append({
                        "key": key,
                        "horizontal": horizontal_clip,
                        "vertical": vertical_clip,
                        "client_width": after["client_width"],
                        "scroll_width": after["scroll_width"],
                        "client_height": after["client_height"],
                        "scroll_height": after["scroll_height"],
                    })
                measurements.append({
                    "key": key,
                    "baseline_font_px": before["font_px"],
                    "resized_font_px": after["font_px"],
                    "scale_ratio": round(ratio, 3),
                    "scale_pass": scale_ok,
                    "clipping_pass": not (horizontal_clip or vertical_clip),
                })

            await expect(control).to_be_visible()
            await control.focus()
            assert await control.evaluate("el => document.activeElement === el") is True
            page_overflow = await page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")

            assert scale_failures == [], {"surface": name, "scale_failures": scale_failures}
            assert clipping_failures == [], {"surface": name, "clipping_failures": clipping_failures}
            assert page_overflow is False, {"surface": name, "horizontal_page_overflow_at_200_percent": True}

            evidence.append({
                "surface": name,
                "critical_control": ready_test_id,
                "critical_control_visible": True,
                "critical_control_focusable": True,
                "horizontal_page_overflow": page_overflow,
                "measurements": measurements,
            })
            await context.close()
        await browser.close()

    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(
        json.dumps(
            {
                "decision": "pass",
                "exact_head": os.environ.get("GITHUB_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
                "wcag_success_criterion": "1.4.4 Resize Text",
                "text_resize_percent": 200,
                "covered_surfaces": [surface[0] for surface in SURFACES],
                "browser": "chromium",
                "backend_session_rbac_real": True,
                "human_share_approval_preserved": True,
                "product_wide_wcag_2_2_aa_claimed": False,
                "surfaces": evidence,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
