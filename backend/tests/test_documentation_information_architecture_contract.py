from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCH = ROOT / "docs/DOCUMENTATION_INFORMATION_ARCHITECTURE.md"
PORTAL = ROOT / "docs/README.md"


def test_documentation_information_architecture_separates_stable_and_lifecycle_domains():
    text = ARCH.read_text(encoding="utf-8").lower()
    for marker in (
        "stable product and operator domains",
        "lifecycle, quality and evidence domains",
        "installation/",
        "user/",
        "operations/",
        "architecture/",
        "security/",
        "governance/",
        "project/",
        "roadmap/",
        "qa/",
        "evidence/",
        "repository ci is repository evidence only",
        "historical evidence is preserved",
        "server-side credential boundaries",
    ):
        assert marker in text, marker


def test_documentation_portal_preserves_stable_vs_history_boundary():
    text = PORTAL.read_text(encoding="utf-8")
    assert "organized around what readers need to do rather than around internal delivery chronology" in text
    assert "Detailed project chronology belongs" in text
    assert "exact run history belongs in evidence records rather than product-facing navigation" in text
    assert "Repository CI is engineering evidence" in text
    assert "not production authorized" in text
