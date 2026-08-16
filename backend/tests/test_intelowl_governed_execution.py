from __future__ import annotations

import pytest
from fastapi.routing import APIRoute

from dtmo.config import Settings
from dtmo.integrations.intelowl import IntelOwlAdapter, IntelOwlPolicyError
from dtmo.intelowl_execution import IntelOwlExecutionRequest, router
from dtmo.persistence.models import IntelOwlEnrichmentRecord


def test_intelowl_history_model_enforces_authority_invariants() -> None:
    table = IntelOwlEnrichmentRecord.__table__
    names = {constraint.name for constraint in table.constraints}

    assert "uq_intelowl_enrichment_item_job" in names
    assert "ck_intelowl_enrichment_no_share_authority" in names
    assert "ck_intelowl_enrichment_no_compromise_proof" in names
    assert table.c.external_share_authorized.default.arg is False
    assert table.c.local_compromise_proven.default.arg is False


def test_governed_routes_are_bounded_to_item_execution_and_history() -> None:
    routes = {
        (route.path, tuple(sorted(route.methods or set())))
        for route in router.routes
        if isinstance(route, APIRoute)
    }

    assert ("/api/v1/intelowl/items/{item_id}/enrich", ("POST",)) in routes
    assert ("/api/v1/intelowl/items/{item_id}/history", ("GET",)) in routes


def test_execution_request_requires_analyzers() -> None:
    with pytest.raises(ValueError):
        IntelOwlExecutionRequest(
            observable_type="cve",
            observable_value="CVE-2026-12345",
            handling="amber",
            analyzers=[],
        )


def test_restricted_handling_fails_closed_for_separate_service_analyzers() -> None:
    settings = Settings(
        intelowl_allowed_observable_types="cve,ip,domain,url,hash",
        intelowl_allowed_analyzers="vulnerability_lookup",
    )
    adapter = IntelOwlAdapter(settings)

    with pytest.raises(IntelOwlPolicyError, match="forbids external analyzer disclosure"):
        adapter._validate_request(
            observable_type="cve",
            observable_value="CVE-2026-12345",
            handling="tlp:red",
            analyzers=["vulnerability_lookup"],
            external_analyzers={"vulnerability_lookup"},
        )
