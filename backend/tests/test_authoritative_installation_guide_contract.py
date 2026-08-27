from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GUIDE = ROOT / "docs/installation/INSTALLATION_GUIDE.md"
ROOT_README = ROOT / "README.md"
DOCS_README = ROOT / "docs/README.md"
CURRENT_STATE = ROOT / "docs/project/CURRENT_STATE.md"


def test_authoritative_installation_guide_covers_clean_supported_path_and_boundaries():
    text = GUIDE.read_text(encoding="utf-8")
    for marker in (
        "single authoritative installation guide",
        "python3 tools/bootstrap_local.py",
        "docker compose up --build",
        "AISTOR_IMAGE",
        "AISTOR_LICENSE_FILE",
        "http://localhost:8000/",
        "http://localhost:8080/",
        "First administration workflow",
        "First-data workflow",
        "CLEAN_INSTALL_OWNER_RETEST_RUNBOOK.md",
        "credentials stay server-side",
        "fails closed",
        "not production authorized",
        "not staging acceptance",
        "not production-equivalent validation",
        "independent assurance",
    ):
        assert marker.lower() in text.lower(), marker


def test_installation_guide_is_discoverable_from_primary_documentation_entrypoints():
    root = ROOT_README.read_text(encoding="utf-8")
    docs = DOCS_README.read_text(encoding="utf-8")
    assert "docs/installation/INSTALLATION_GUIDE.md" in root
    assert "installation/INSTALLATION_GUIDE.md" in docs


def test_current_state_tracks_installation_guide_as_completed_repository_preparation():
    text = CURRENT_STATE.read_text(encoding="utf-8")
    assert "single authoritative local/reference installation procedure" in text.lower()
    assert "docs/installation/INSTALLATION_GUIDE.md" in text
    assert "clean-install owner retest" in text.lower()
    assert "candidate freeze" in text.lower()
