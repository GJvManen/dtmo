from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))
EVIDENCE_PATH = Path(
    os.environ.get(
        "DTMO_CONTRAST_EVIDENCE_PATH",
        "artifacts/browser-contrast-measurements.json",
    )
)

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.11 contrast E2E executes only in the dedicated browser workflow",
)

SURFACES = (
    ("share_approval", "/ui/share-approval", "contrast-admin", "admin", "review-button"),
    ("analyst_search", "/ui/analyst-search", "contrast-analyst", "analyst", "search-submit"),
    ("ciso_token_revocation", "/ui/ciso-security", "contrast-ciso", "ciso", "revoke-submit"),
    ("auditor_read_only", "/ui/auditor", "contrast-auditor", "auditor", "load-audit"),
)

MEASURE_PAGE_SCRIPT = r"""() => {
  const textSelectors = 'h1,h2,h3,h4,h5,h6,p,label,button,legend,pre,[role="status"],li,strong,code';
  const controlSelectors = 'button,input,textarea,select,a[href]';

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

  function visible(el) {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
  }

  function key(el) {
    return el.getAttribute('data-testid') || el.id || null;
  }

  const text = [];
  for (const el of document.querySelectorAll(textSelectors)) {
    if (!visible(el)) continue;
    const style = getComputedStyle(el);
    const value = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
    if (!value) continue;

    const bg = effectiveBackground(el);
    const rawFg = parseColor(style.color);
    const fg = rawFg.a < 1 ? blend(rawFg, bg) : rawFg;
    const fontPx = Number.parseFloat(style.fontSize);
    const weight = style.fontWeight === 'bold' ? 700 : Number.parseInt(style.fontWeight, 10) || 400;
    const large = fontPx >= 24 || (fontPx >= 18.5 && weight >= 700);
    const minimum = large ? 3.0 : 4.5;
    const measured = ratio(fg, bg);
    text.push({
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      testid: el.getAttribute('data-testid'),
      text: value.slice(0, 120),
      color: style.color,
      background: `rgb(${Math.round(bg.r)}, ${Math.round(bg.g)}, ${Math.round(bg.b)})`,
      font_px: fontPx,
      font_weight: weight,
      large_text: large,
      minimum_ratio: minimum,
      measured_ratio: Number(measured.toFixed(3)),
      pass: measured + 1e-9 >= minimum,
    });
  }

  const controls = [];
  for (const el of document.querySelectorAll(controlSelectors)) {
    if (!visible(el) || el.disabled) continue;
    const style = getComputedStyle(el);
    const controlBg = effectiveBackground(el);
    const outerBg = effectiveBackground(el.parentElement || document.body);
    const fillRatio = ratio(controlBg, outerBg);
    const borderRatios = [];
    for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
      const width = Number.parseFloat(style[`border${side}Width`]);
      const borderStyle = style[`border${side}Style`];
      if (width > 0 && borderStyle !== 'none' && borderStyle !== 'hidden') {
        const raw = parseColor(style[`border${side}Color`]);
        const color = raw.a < 1 ? blend(raw, outerBg) : raw;
        borderRatios.push(ratio(color, outerBg));
      }
    }
    const borderRatio = borderRatios.length ? Math.min(...borderRatios) : 0;
    const measured = Math.max(fillRatio, borderRatio);
    controls.push({
      key: key(el),
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      testid: el.getAttribute('data-testid'),
      fill_ratio: Number(fillRatio.toFixed(3)),
      border_ratio: Number(borderRatio.toFixed(3)),
      measured_boundary_ratio: Number(measured.toFixed(3)),
      minimum_ratio: 3.0,
      pass: measured + 1e-9 >= 3.0,
    });
  }

  return {text, controls};
}"""

FOCUS_MEASURE_SCRIPT = r"""() => {
  const el = document.activeElement;
  if (!el || !el.matches('button,input,textarea,select,a[href]')) return null;

  function parseColor(value) {
    const match = value.match(/rgba?\(([^)]+)\)/);
    if (!match) throw new Error(`unsupported color: ${value}`);
    const parts = match[1].split(',').map(part => Number.parseFloat(part.trim()));
    return {r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1};
  }
  function blend(fg, bg) {
    const a = fg.a + bg.a * (1 - fg.a);
    if (a === 0) return {r:255,g:255,b:255,a:1};
    return {
      r:(fg.r*fg.a + bg.r*bg.a*(1-fg.a))/a,
      g:(fg.g*fg.a + bg.g*bg.a*(1-fg.a))/a,
      b:(fg.b*fg.a + bg.b*bg.a*(1-fg.a))/a,
      a,
    };
  }
  function effectiveBackground(node) {
    const layers = [];
    while (node) {
      const style = getComputedStyle(node);
      if (style.backgroundImage !== 'none') throw new Error(`background image unsupported on ${node.tagName}`);
      layers.push(parseColor(style.backgroundColor));
      node = node.parentElement;
    }
    let bg = {r:255,g:255,b:255,a:1};
    for (let i = layers.length - 1; i >= 0; i -= 1) bg = blend(layers[i], bg);
    return bg;
  }
  function channel(value) {
    const c = value / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  }
  function luminance(color) {
    return 0.2126*channel(color.r) + 0.7152*channel(color.g) + 0.0722*channel(color.b);
  }
  function ratio(a,b) {
    const l1=luminance(a), l2=luminance(b);
    return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
  }

  const style = getComputedStyle(el);
  const width = Number.parseFloat(style.outlineWidth);
  const hasOutline = width > 0 && style.outlineStyle !== 'none' && style.outlineStyle !== 'hidden';
  if (!hasOutline) {
    return {
      key: el.getAttribute('data-testid') || el.id || null,
      outline_style: style.outlineStyle,
      outline_width: style.outlineWidth,
      measured_focus_ratio: 0,
      minimum_ratio: 3.0,
      pass: false,
    };
  }
  const outerBg = effectiveBackground(el.parentElement || document.body);
  const controlBg = effectiveBackground(el);
  const raw = parseColor(style.outlineColor);
  const outline = raw.a < 1 ? blend(raw, outerBg) : raw;
  const outerRatio = ratio(outline, outerBg);
  const innerRatio = ratio(outline, controlBg);
  const measured = Math.min(outerRatio, innerRatio);
  return {
    key: el.getAttribute('data-testid') || el.id || null,
    outline_style: style.outlineStyle,
    outline_width: style.outlineWidth,
    outline_color: style.outlineColor,
    against_outer_ratio: Number(outerRatio.toFixed(3)),
    against_control_ratio: Number(innerRatio.toFixed(3)),
    measured_focus_ratio: Number(measured.toFixed(3)),
    minimum_ratio: 3.0,
    pass: measured + 1e-9 >= 3.0,
  };
}"""


@pytest.mark.asyncio
async def test_measured_text_ui_and_focus_contrast_on_critical_surfaces() -> None:
    all_measurements: list[dict[str, object]] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for name, path, subject, roles, ready_test_id in SURFACES:
            context = await browser.new_context(
                extra_http_headers={"X-DTMO-Subject": subject, "X-DTMO-Roles": roles}
            )
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{path}")
            assert response is not None and response.ok, {
                "surface": name,
                "status": None if response is None else response.status,
            }

            principal = page.locator(
                '[data-testid="principal"], [data-testid="analyst-principal"], '
                '[data-testid="ciso-principal"], [data-testid="auditor-principal"]'
            )
            await expect(principal).to_contain_text(subject)
            await expect(page.get_by_test_id(ready_test_id)).to_be_visible()

            page_measurements = await page.evaluate(MEASURE_PAGE_SCRIPT)
            text_measurements = page_measurements["text"]
            control_measurements = page_measurements["controls"]
            assert text_measurements, f"no rendered text contrast measurements captured for {name}"
            assert control_measurements, f"no visible UI controls measured for {name}"
            assert [row for row in text_measurements if not row["pass"]] == [], {
                "surface": name,
                "text_contrast_failures": [row for row in text_measurements if not row["pass"]],
            }
            assert [row for row in control_measurements if not row["pass"]] == [], {
                "surface": name,
                "ui_boundary_contrast_failures": [row for row in control_measurements if not row["pass"]],
            }

            expected_keys = {row["key"] for row in control_measurements if row["key"]}
            focus_measurements: list[dict[str, object]] = []
            seen: set[str] = set()
            for _ in range(len(expected_keys) + 8):
                await page.keyboard.press("Tab")
                row = await page.evaluate(FOCUS_MEASURE_SCRIPT)
                if not row or not row["key"] or row["key"] in seen:
                    continue
                if row["key"] in expected_keys:
                    focus_measurements.append(row)
                    seen.add(row["key"])
                if seen == expected_keys:
                    break

            assert seen == expected_keys, {
                "surface": name,
                "expected_focus_controls": sorted(expected_keys),
                "measured_focus_controls": sorted(seen),
            }
            assert [row for row in focus_measurements if not row["pass"]] == [], {
                "surface": name,
                "focus_contrast_failures": [row for row in focus_measurements if not row["pass"]],
            }

            all_measurements.append(
                {
                    "surface": name,
                    "text_measurements": text_measurements,
                    "ui_boundary_measurements": control_measurements,
                    "focus_indicator_measurements": focus_measurements,
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
                "wcag_success_criteria": [
                    "1.4.3 Contrast (Minimum)",
                    "1.4.11 Non-text Contrast",
                ],
                "normal_text_minimum_ratio": 4.5,
                "large_text_minimum_ratio": 3.0,
                "ui_component_minimum_ratio": 3.0,
                "focus_indicator_minimum_ratio": 3.0,
                "covered_surfaces": [surface[0] for surface in SURFACES],
                "browser": "chromium",
                "backend_session_rbac_real": True,
                "human_share_approval_preserved": True,
                "product_wide_wcag_2_2_aa_claimed": False,
                "surfaces": all_measurements,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
