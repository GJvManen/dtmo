from pathlib import Path

from dtmo.config import Settings
from dtmo.integration_readiness import integration_readiness
from dtmo.source_catalog import SOURCE_CATALOG

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "frontend/src/main.tsx"
READINESS_COMPONENT = ROOT / "frontend/src/FrameworkIntegrationReadiness.tsx"


def test_governed_source_catalog_provides_meaningful_bootstrap_content():
    ids = {item.id for item in SOURCE_CATALOG}
    assert len(SOURCE_CATALOG) >= 15
    assert {"cisa-kev", "nvd-cve", "github-global-advisories", "ncsc-nl-advisories", "cert-eu-advisories"} <= ids
    assert all(item.provenance_note.strip() for item in SOURCE_CATALOG)
    assert all(item.endpoint_url.startswith("https://") for item in SOURCE_CATALOG)


def test_default_integrations_explain_disabled_readiness_instead_of_implying_missing_capability():
    rows = {row.id: row for row in integration_readiness(Settings())}
    assert {"misp", "ail", "taranis", "intelowl", "cortex", "opencti", "thehive"} <= rows.keys()
    assert all(row.state == "disabled" for row in rows.values())
    assert all("Capability exists" in row.detail for row in rows.values())
    assert all(row.action.startswith("Configure") for row in rows.values())


def test_readiness_distinguishes_endpoint_credential_and_enabled_state():
    endpoint_only = Settings(feature_misp_connector=True, misp_api_base="https://misp.example")
    assert {row.id: row for row in integration_readiness(endpoint_only)}["misp"].state == "credential-required"

    enabled_without_endpoint = Settings(feature_opencti_read=True)
    assert {row.id: row for row in integration_readiness(enabled_without_endpoint)}["opencti"].state == "configuration-required"

    ready = Settings(feature_misp_connector=True, misp_api_base="https://misp.example", misp_api_key="runtime-secret")
    assert {row.id: row for row in integration_readiness(ready)}["misp"].state == "ready"


def test_canonical_administration_mounts_explicit_framework_activation_readiness():
    main = MAIN.read_text(encoding="utf-8")
    readiness = READINESS_COMPONENT.read_text(encoding="utf-8")
    assert "import { FrameworkIntegrationReadiness }" in main
    assert "<AdministrationWorkspace /><FrameworkIntegrationReadiness /><AdministrationSecurityAudit />" in main
    assert "'/api/v1/admin/integrations'" in readiness
    assert "method: 'PATCH'" in readiness
    assert "X-Request-ID" in readiness
    assert "Explicit activation · no auto-enable" in readiness
    assert "configured · activation required" in readiness
    assert "runtime health is not implied" in readiness
    assert "Component-specific scopes, analyzer allowlists, organization settings and upstream reachability" in readiness
