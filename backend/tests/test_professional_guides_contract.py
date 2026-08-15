from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "docs/product/PRODUCT_GUIDE.md"
USER = ROOT / "docs/user/USER_GUIDE.md"
ADMIN = ROOT / "docs/administration/ADMINISTRATOR_GUIDE.md"
PORTAL = ROOT / "docs/README.md"
SCREENSHOTS = ROOT / "docs/visual/screenshots/README.md"
SCREENSHOT_ROOT = ROOT / "docs/visual/screenshots"

PUBLISHED_SCREENSHOTS = (
    "overview-dashboard.png",
    "intelligence-workspace.png",
    "sources-catalogue.png",
    "vulnerability-analytics.png",
    "ail-correlation-workspace.png",
    "visual-analytics.png",
    "governance-frameworks.png",
    "administration-rbac.png",
)


def test_professional_guides_exist_and_preserve_claim_boundaries() -> None:
    for path in (PRODUCT, USER, ADMIN):
        text = path.read_text(encoding="utf-8")
        assert "SYSTEM_WORKFLOWS.md" in text
        assert "screenshot" in text.lower()
        assert "production" in text.lower()
        assert "```mermaid" in text

    product = PRODUCT.read_text(encoding="utf-8")
    assert "DTMO is **not production ready**" in product
    assert "does not independently prove exploitability" in product

    user = USER.read_text(encoding="utf-8")
    assert "does not prove live source connectivity" in user
    assert "does not change the source classification" in user

    admin = ADMIN.read_text(encoding="utf-8")
    assert "UI visibility is never the final authorization decision" in admin
    assert "Production credentials must not be reused" in admin


def test_documentation_portal_exposes_audience_guides() -> None:
    text = PORTAL.read_text(encoding="utf-8")
    for link in (
        "product/PRODUCT_GUIDE.md",
        "user/USER_GUIDE.md",
        "administration/ADMINISTRATOR_GUIDE.md",
    ):
        assert link in text
    assert "base screenshot capture has been exercised successfully in CI" in text


def test_screenshot_catalogue_tracks_published_and_pending_surfaces() -> None:
    text = SCREENSHOTS.read_text(encoding="utf-8")
    assert "base runtime capture validated" in text
    assert "UI-05" in text and "capture contract added / CI validation pending" in text
    assert "UI-10" in text and "capture validated; repository promotion pending" in text
    assert "A diagram or API contract must never be promoted as a product screenshot" in text

    for name in PUBLISHED_SCREENSHOTS:
        assert name in text
        path = SCREENSHOT_ROOT / name
        assert path.is_file(), name
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), name
        assert len(data) > 10_000, name


def test_markdown_screenshot_references_resolve_to_repository_files() -> None:
    for document in (PRODUCT, USER, ADMIN, SCREENSHOTS):
        text = document.read_text(encoding="utf-8")
        image_targets = re.findall(r"!\[[^\]]*\]\(([^)]+\.png)\)", text)
        assert image_targets, document
        for target in image_targets:
            resolved = (document.parent / target).resolve()
            assert resolved.is_relative_to(ROOT), (document, target)
            assert resolved.is_file(), (document, target)
            assert resolved.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), (document, target)
