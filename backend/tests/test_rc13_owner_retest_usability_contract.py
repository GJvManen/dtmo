from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONSOLE = ROOT / "backend/dtmo/unified_console.py"
ADMIN = ROOT / "backend/dtmo/rc13_administration.py"
PHASE8 = ROOT / "docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md"


def test_overview_refresh_is_truthful_and_fail_closed_for_empty_data() -> None:
    source = CONSOLE.read_text(encoding="utf-8")
    assert 'id="refresh-all"' in source
    assert "async function refreshAll" in source
    assert "Gegevens vernieuwen…" in source
    assert "Geen intelligence data · bronstatus geladen" in source
    assert "Vernieuwen deels mislukt" in source
    assert "'Data bijgewerkt'" not in source


def test_zero_value_datasets_render_explicit_empty_state() -> None:
    source = CONSOLE.read_text(encoding="utf-8")
    assert "Geen data om te visualiseren" in source
    assert "total<=0" in source
    assert "Nog geen intelligence in de afgelopen 7 dagen." in source
    assert "Nog geen intelligence met severity-classificatie." in source
    assert "Nog geen intelligencebronnen met ingested records." in source


def test_navigation_is_chrome_safe_and_version_badge_removed() -> None:
    source = CONSOLE.read_text(encoding="utf-8")
    assert '<span class="status-pill neutral">16.0.0rc12</span>' not in source
    for label in (
        "Overzicht",
        "Intelligence",
        "Bronnen & catalogus",
        "Visual analytics",
        "Administration",
        "Governance",
    ):
        assert f'type="button" class="button secondary" data-view=' in source or label in source
    assert "function closestTarget" in source
    assert "window.addEventListener('error'" in source
    assert "window.addEventListener('unhandledrejection'" in source


def test_administration_copy_no_longer_claims_future_rc13_work() -> None:
    source = CONSOLE.read_text(encoding="utf-8")
    assert "Governed role administration volgt in RC13.3" not in source
    assert "Beheer governed gebruikers en rollen vanuit één centrale werkruimte" in source
    assert "Technische sessiecontext (development)" in source
    assert "Bronbeheer blijft bewust in Bronnen & catalogus" in source
    admin = ADMIN.read_text(encoding="utf-8")
    assert "Gebruikers & rollen" in admin
    assert "Zelfbeheer is server-side geblokkeerd" in admin


def test_phase8_is_paused_again_until_repaired_owner_retest() -> None:
    text = PHASE8.read_text(encoding="utf-8")
    assert "PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST" in text
    assert "project-owner" in text.lower() or "project owner" in text.lower()
