from __future__ import annotations

import pytest

from dtmo.admin_sources import bootstrap_supported_sources
from dtmo.auth.policy import Principal, Role
from dtmo.source_catalog import CISCO_CREDENTIAL_REFERENCE, SOURCE_CATALOG
from dtmo.sources import SourceDefinition, validate_secret_ref


class _FakeSession:
    def __init__(self) -> None:
        self.sources: dict[str, SourceDefinition] = {}

    async def get(self, model, source_id: str):
        assert model is SourceDefinition
        return self.sources.get(source_id)

    def add(self, source: SourceDefinition) -> None:
        self.sources[source.id] = source

    async def flush(self) -> None:
        return None

    async def run_sync(self, fn):
        # The bootstrap contract under test is registry/catalog compatibility.
        # Persistent audit behavior is covered by the existing admin-source gates.
        return None


def test_every_supported_catalog_secret_ref_is_registry_compatible() -> None:
    for entry in SOURCE_CATALOG:
        if entry.execution_status != "supported" or entry.secret_ref is None:
            continue
        assert validate_secret_ref(entry.secret_ref) == entry.secret_ref


@pytest.mark.asyncio
async def test_supported_catalog_bootstrap_is_idempotent_and_keeps_sources_disabled() -> None:
    session = _FakeSession()
    principal = Principal(subject="owner-retest-admin", roles=frozenset({Role.ADMIN}))

    first = await bootstrap_supported_sources(
        principal=principal,
        session=session,
        request_id="rc13-source-catalog-bootstrap-1",
    )
    second = await bootstrap_supported_sources(
        principal=principal,
        session=session,
        request_id="rc13-source-catalog-bootstrap-2",
    )

    expected = {entry.id for entry in SOURCE_CATALOG if entry.execution_status == "supported"}
    assert {source.id for source in first} == expected
    assert {source.id for source in second} == expected
    assert set(session.sources) == expected
    assert all(source.enabled is False for source in session.sources.values())
    assert session.sources["cisco-security-advisories"].secret_ref == CISCO_CREDENTIAL_REFERENCE
    assert CISCO_CREDENTIAL_REFERENCE == "env:CISCO_OPENVULN_TOKEN"
