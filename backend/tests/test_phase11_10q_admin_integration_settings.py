from pathlib import Path

import dtmo.admin_center as admin
from dtmo.config import Settings


def test_integration_settings_are_actionable_and_never_return_secret_values(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(admin, "settings", Settings())
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", tmp_path / "runtime-integration-settings.json")

    before = {row["id"]: row for row in admin.list_integrations(None)}
    assert before["misp"]["state"] == "disabled"
    assert "credential_boundary" in before["misp"]
    assert "api_key" not in before["misp"]
    assert "token" not in before["misp"]

    updated = admin.update_integration(
        "misp",
        admin.IntegrationPatch(enabled=True, api_base="https://misp.example/api/"),
        None,
    )
    assert updated["enabled"] is True
    assert updated["api_base"] == "https://misp.example/api"
    assert updated["state"] == "credential-required"
    assert admin._RUNTIME_CONFIG_PATH.exists()
    document = admin._RUNTIME_CONFIG_PATH.read_text(encoding="utf-8")
    assert "misp.example/api" in document
    assert "runtime-secret" not in document


def test_persisted_nonsecret_configuration_is_reapplied(tmp_path: Path, monkeypatch):
    path = tmp_path / "runtime-integration-settings.json"
    path.write_text('{"opencti":{"enabled":true,"api_base":"https://opencti.example"}}', encoding="utf-8")
    settings = Settings()
    monkeypatch.setattr(admin, "settings", settings)
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", path)

    admin._apply_persisted_runtime_configuration()
    assert settings.feature_opencti_read is True
    assert settings.opencti_api_base == "https://opencti.example"


def test_unknown_integration_fails_closed(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(admin, "settings", Settings())
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    try:
        admin.update_integration("unknown", admin.IntegrationPatch(enabled=True), None)
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 404
    else:
        raise AssertionError("unknown integration must fail closed")
