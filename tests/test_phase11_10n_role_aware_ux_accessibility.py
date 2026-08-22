from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "architecture" / "PHASE11_10N_ROLE_AWARE_UX_ACCESSIBILITY.md"
WORKFLOW = ROOT / ".github" / "workflows" / "phase11-role-aware-ux-accessibility.yml"


def test_phase11_10n_contract_exists_and_preserves_server_side_authority():
    text = ARCH.read_text(encoding="utf-8")
    required = [
        "Role-aware UX & Accessibility",
        "server-side identity/RBAC/policy enforcement",
        "hidden or disabled UI never substitutes for server authorization",
        "unavailable or unknown capability state fails closed",
        "service accounts never receive human-only review/share/publication authority",
        "Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**",
    ]
    for marker in required:
        assert marker in text


def test_phase11_10n_accessibility_acceptance_is_explicit():
    text = ARCH.read_text(encoding="utf-8")
    required = [
        "keyboard-only navigation",
        "visible focus order",
        "semantic landmarks",
        "accessible names",
        "non-color-only communication",
        "text resize",
        "reflow",
        "text-spacing resilience",
        "assistive technology",
        "supported-browser behavior",
    ]
    for marker in required:
        assert marker in text


def test_phase11_10n_evidence_boundary_and_next_slice_are_fail_closed():
    text = ARCH.read_text(encoding="utf-8")
    assert "Repository CI is engineering evidence only" in text
    assert "Screenshots and browser tests do not prove production identity-provider behavior" in text
    assert "Phase 11.10o consolidation / full functional acceptance" in text
    assert "Phase 11.10p production-equivalent validation remains prohibited" in text


def test_phase11_10n_has_dedicated_exact_head_workflow():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 11 Role-aware UX Accessibility Gate" in text
    assert "tests/test_phase11_10n_role_aware_ux_accessibility.py" in text
    assert "pytest -q" in text
