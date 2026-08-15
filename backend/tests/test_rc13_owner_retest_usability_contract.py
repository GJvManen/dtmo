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
    for label, view in (
        ("Overzicht", "overview"),
        ("Intelligence", "intelligence"),
        ("Bronnen & catalogus", "sources"),
        ("Visual analytics", "analytics"),
        ("Administration", "administration"),
        ("Governance", "governance"),
    ):
        expected = (
            f'type="button" class="button secondary" data-view="{view}">{label}</button>'
        )
        assert expected in source
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


def test_phase8_proceeds_with_owner_approved_staging_without_weakening_identity_gate() -> None:
    text = PHASE8.read_text(encoding="utf-8")
    assert "ACTIVE_EXTERNAL_VALIDATION / OWNER_APPROVED_STAGING / IMMUTABLE_EVIDENCE_BINDING_INCOMPLETE" in text
    assert "RC13 functional console: `PASS / OWNER_ACCEPTED`" in text
    assert "post-E8 external deployment: `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`" in text
    assert "production-equivalent staging environment: `APPROVED / OWNER_VERIFIED_EXTERNAL_EVIDENCE`" in text
    assert "Formal Phase 8 closure still requires that the accepted deployment be bound to one immutable technical identity" in text
    assert "Phase 8 is complete only when the immutable staging identity is complete and approved" in text
    assert "Repository CI, local Docker Compose, staging emulators and synthetic browser fixtures cannot satisfy this gate by themselves" in text
