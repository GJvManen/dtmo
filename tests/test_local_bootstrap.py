from pathlib import Path


def test_bootstrap_helper_documents_required_fail_fast_contract():
    text = Path("tools/bootstrap_local.py").read_text(encoding="utf-8")
    assert "Docker daemon is not running" in text
    assert "AISTOR_IMAGE" in text
    assert "AISTOR_LICENSE_FILE" in text
    assert "docker compose config" in text
    assert "GRAFANA_DB_PASSWORD" in text


def test_readme_uses_bootstrap_helper_for_fresh_clone():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "python3 tools/bootstrap_local.py" in text
    assert "ACTION REQUIRED" in text
