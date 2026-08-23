from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/CollectionWorkspace.tsx"
API = ROOT / "backend/dtmo/admin_sources.py"


def test_collection_workspace_exposes_complete_same_origin_operator_journey() -> None:
    text = WORKSPACE.read_text(encoding="utf-8")
    for marker in (
        "'/api/v1/admin/sources'",
        "'/api/v1/admin/sources/catalog'",
        "'/api/v1/admin/sources/catalog/bootstrap'",
        "Register source",
        "Register disabled source",
        "'PATCH'",
        "'validate'",
        "'test'",
        "'run'",
        "credentials: 'same-origin'",
        "manage:connectors",
        "Reference only; never enter a raw API key or password.",
        "All registered sources",
    ):
        assert marker in text


def test_collection_api_supports_registration_activation_validation_test_and_run() -> None:
    text = API.read_text(encoding="utf-8")
    for marker in (
        '@router.post("", response_model=SourceResponse',
        '@router.patch("/{source_id}"',
        '@router.post("/{source_id}/validate")',
        '@router.post("/{source_id}/test")',
        '@router.post("/{source_id}/run")',
        '@router.post("/catalog/bootstrap"',
        "Permission.MANAGE_CONNECTORS",
        "new manual sources must be created disabled",
        "source registry changes require a human admin role",
        "publication_gate",
    ):
        assert marker in text


def test_collection_evidence_boundary_remains_fail_closed() -> None:
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "Connectivity, successful testing or ingestion proves only the recorded collection action" in text
    assert "Neither proves source truth, compromise, review completion, external-share authority, production readiness or publication authorization" in text
