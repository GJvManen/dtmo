from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))
EVIDENCE_PATH = Path(os.environ.get("DTMO_CONTRAST_EVIDENCE_PATH", "artifacts/browser-text-contrast-measurements.json"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.11 text-contrast E2E executes only in the dedicated browser workflow",
)

SURFACES = (
    ("share_approval", "/ui/share-approval", "contrast-admin", "admin", "review-button"),
    ("analyst_search", "/ui/analyst-search", "contrast-analyst", "analyst", "search-submit"),
    ("ciso_token_revocation", "/ui/ciso-security", "contrast-ciso", "ciso", "revoke-submit"),
    ("auditor_read_only", "/ui/auditor", "contrast-auditor", "auditor", "load-audit"),
)

MEASURE_SCRIPT = r"""() => {
  const selectors = 'h1,h2,h3,h4,h5,h6,p,label,button,legend,pre,[role="status"],li,strong,code';

  function parseColor(value) {
    const match = value.match(/rgba?\(([^)]+)\)/);
    if (!match) throw new Error(`unsupported color: ${value}`);
    const parts = match[1].split(',').map(part => Number.parseFloat(part.trim()));
    return {r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1};
  }

  function blend(fg, bg) {
    const a = fg.a + bg.a * (1 - fg.a);
    if (a === 0) return {r: 255, g: 255, b: 255, a: 1};
    return {
      r: (fg.r * fg.a + bg.r * bg.a * (1 - fg.a)) / a,
      g: (fg.g * fg.a + bg.g * bg.a * (1 - fg.a)) / a,
      b: (fg.b * fg.a + bg.b * bg.a * (1 - fg.a)) / a,
      a,
    };
  }

  function effectiveBackground(el) {
    const layers = [];
    let node = el;
    while (node) {
      const style = getComputedStyle(node);
      if (style.backgroundImage !== 'none') {
        throw new Error(`background image unsupported for contrast measurement on ${node.tagName}`);
      }
      layers.push(parseColor(style.backgroundColor));
      node = node.parentElement;
    }
    let bg = {r: 255, g: 255, b: 255, a: 1};
    for (let i = layers.length - 1; i >= 0; i -= 1) bg = blend(layers[i], bg);
    return bg;
  }

  function channel(value) {
    const c = value / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  }

  function luminance(color) {
    return 0.2126 * channel(color.r) + 0.7152 * channel(color.g) + 0.0722 * channel(color.b);
  }

  function ratio(a, b) {
    const l1 = luminance(a);
    const l2 = luminance(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }

  const rows = [];
  for (const el of document.querySelectorAll(selectors)) {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const text = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
    if (!text || rect.width === 0 || rect.height === 0 || style.visibility === 'hidden' || style.display === 'none') continue;

    const bg = effectiveBackground(el);
    const rawFg = parseColor(style.color);
    const fg = rawFg.a < 1 ? blend(rawFg, bg) : rawFg;
    const fontPx = Number.parseFloat(style.fontSize);
    const weightRaw = style.fontWeight === 'bold' ? 700 : Number.parseInt(style.fontWeight, 10) || 400;
    const large = fontPx >= 24 || (fontPx >= 18.5 && weightRaw >= 700);
    const minimum = large ? 3.0 : 4.5;
    const measured = ratio(fg, bg);
    rows.push({
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      testid: el.getAttribute('data-testid'),
      text: text.slice(0, 120),
      color: style.color,
      background: `rgb(${Math.round(bg.r)}, ${Math.round(bg.g)}, ${Math.round(bg.b)})`,
      font_px: fontPx,
      font_weight: weightRaw,
      large_text: large,
      minimum_ratio: minimum,
      measured_ratio: Number(measured.toFixed(3)),
      pass: measured + 1e-9 >= minimum,
    });
  }
  return rows;
}"""


@pytest.mark.asyncio
async def test_wcag_1_4_3_measured_text_contrast_on_critical_surfaces() -> None:
    all_measurements: list[dict[str, object]] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for name, path, subject, roles, ready_test_id in SURFACES:
            context = await browser.new_context(
                extra_http_headers={"X-DTMO-Subject": subject, "X-DTMO-Roles": roles}
            )
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{path}")
            assert response is not None and response.ok, {"surface": name, "status": None if response is None else response.status}

            principal = page.locator('[data-testid$="principal"], [data-testid="principal"]')
            await expect(principal).to_contain_text(subject)
            await expect(page.get_by_test_id(ready_test_id)).to_be_visible()

            measurements = await page.evaluate(MEASURE_SCRIPT)
            assert measurements, f"no rendered text contrast measurements captured for {name}"
            failures = [row for row in measurements if not row["pass"]]
            assert failures == [], {"surface": name, "contrast_failures": failures}
            all_measurements.append({"surface": name, "measurements": measurements})
            await context.close()
        await browser.close()

    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(
        json.dumps(
            {
                "decision": "pass",
                "exact_head": os.environ.get("GITHUB_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
                "wcag_success_criterion": "1.4.3 Contrast (Minimum)",
                "normal_text_minimum_ratio": 4.5,
                "large_text_minimum_ratio": 3.0,
                "covered_surfaces": [surface[0] for surface in SURFACES],
                "browser": "chromium",
                "backend_session_rbac_real": True,
                "human_share_approval_preserved": True,
                "non_text_contrast_claimed": False,
                "product_wide_wcag_2_2_aa_claimed": False,
                "surfaces": all_measurements,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
