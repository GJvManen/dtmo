from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_collection_workspace_is_canonical_and_server_governed() -> None:
    app = read("frontend/src/App.tsx")
    workspace = read("frontend/src/CollectionWorkspace.tsx")
    admin = read("backend/dtmo/admin_sources.py")

    assert "import { CollectionWorkspace } from './CollectionWorkspace';" in app
    assert "workspace.path === '/collection'" in app
    assert "<CollectionWorkspace />" in app

    for marker in (
        "/api/v1/admin/sources/catalog",
        "/api/v1/admin/sources",
        "manage:connectors",
        "Collection ≠ publication",
        "No healthy or zero-source state is inferred",
        "Connectivity, successful testing or ingestion proves only the recorded collection action",
    ):
        assert marker in workspace

    for marker in (
        "Permission.MANAGE_CONNECTORS",
        "source registry changes require a human admin role",
        "new manual sources must be created disabled",
        "runtime re-resolves DNS",
        "bounded non-ingesting pre-activation test",
        "ConnectorStateStore",
        "human-review-and-separate-share-approval-required",
    ):
        assert marker in admin


def test_collection_credentials_and_authorities_remain_separated() -> None:
    workspace = read("frontend/src/CollectionWorkspace.tsx")
    admin = read("backend/dtmo/admin_sources.py")
    architecture = read("docs/architecture/PHASE11_10J_SOURCES_COLLECTION.md")
    user = read("docs/user/SOURCES_COLLECTION_WORKSPACE.md")

    assert "credential values remain server-side" in workspace
    assert "secret_ref" in admin
    assert "server-side resolution only" in architecture
    assert "Human review/share/case authorities remain separate" in user
    assert "does not prove source truth" in architecture
    assert "production authorization" in architecture


def test_phase11_10j_acceptance_artifacts_exist() -> None:
    for path in (
        ".github/workflows/phase11-sources-collection.yml",
        "backend/tests/test_phase11_10j_sources_collection_contract.py",
        "tests/browser/phase11_10j_collection.py",
        "docs/architecture/PHASE11_10J_SOURCES_COLLECTION.md",
        "docs/qa/PHASE11_10J_SOURCES_COLLECTION_GATE.md",
        "docs/user/SOURCES_COLLECTION_WORKSPACE.md",
    ):
        assert (ROOT / path).is_file(), f"missing Phase 11.10j artifact: {path}"
