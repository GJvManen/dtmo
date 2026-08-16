from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from dtmo.integrations.opencti import OpenCTIItem, OpenCTIPage
from dtmo.persistence.opencti import (
    OpenCTIMappingRevision,
    OpenCTIObjectMapping,
    OpenCTIPersistenceCoordinator,
    mapping_snapshot,
    snapshot_hash,
)


def _item(*, confidence: int = 80, updated_at: str = "2026-08-16T12:10:00Z") -> OpenCTIItem:
    return OpenCTIItem(
        opencti_id="o-1",
        stix_id="indicator--1",
        entity_type="Indicator",
        parent_types=("Stix-Core-Object",),
        markings=({"id": "m-1", "definition_type": "TLP", "definition": "TLP:AMBER"},),
        confidence=confidence,
        created_at="2026-08-16T12:00:00Z",
        updated_at=updated_at,
        external_references=({"id": "r-1", "source_name": "source-a", "url": "https://example.test"},),
        provenance={
            "system": "OpenCTI",
            "boundary": "GraphQL/stixCoreObjects",
            "opencti_id": "o-1",
            "stix_id": "indicator--1",
            "read_only": True,
            "external_share_authorized": False,
            "local_compromise_proven": False,
        },
    )


def test_opencti_mapping_models_enforce_identity_and_authority_invariants() -> None:
    mapping_names = {constraint.name for constraint in OpenCTIObjectMapping.__table__.constraints}
    revision_names = {constraint.name for constraint in OpenCTIMappingRevision.__table__.constraints}

    assert "uq_opencti_mapping_item_opencti" in mapping_names
    assert "uq_opencti_mapping_item_stix" in mapping_names
    assert "ck_opencti_mapping_no_share_authority" in mapping_names
    assert "ck_opencti_mapping_no_compromise_proof" in mapping_names
    assert "uq_opencti_mapping_revision_hash" in revision_names
    assert OpenCTIObjectMapping.__table__.c.external_share_authorized.default.arg is False
    assert OpenCTIObjectMapping.__table__.c.local_compromise_proven.default.arg is False


def test_opencti_snapshot_is_stable_and_keeps_provenance_markings() -> None:
    snapshot = mapping_snapshot(_item())
    assert snapshot["opencti_id"] == "o-1"
    assert snapshot["stix_id"] == "indicator--1"
    assert snapshot["markings"][0]["definition"] == "TLP:AMBER"
    assert snapshot["provenance"]["read_only"] is True
    assert snapshot["external_share_authorized"] is False
    assert snapshot["local_compromise_proven"] is False
    assert snapshot_hash(snapshot) == snapshot_hash(mapping_snapshot(_item()))
    assert snapshot_hash(snapshot) != snapshot_hash(mapping_snapshot(_item(confidence=81)))


@pytest.mark.asyncio
async def test_persistence_coordinator_commits_database_before_checkpoint() -> None:
    events: list[str] = []
    page = OpenCTIPage(items=(_item(),), request_cursor=None, next_cursor=None, has_next_page=False)
    item_id = uuid4()

    session = SimpleNamespace(commit=AsyncMock(side_effect=lambda: events.append("database")))
    adapter = SimpleNamespace(commit_page=lambda received: events.append("checkpoint"))
    coordinator = OpenCTIPersistenceCoordinator(session, adapter)  # type: ignore[arg-type]
    coordinator.repository.persist_page = AsyncMock(return_value=[])  # type: ignore[method-assign]

    await coordinator.persist_and_checkpoint(item_id=item_id, page=page)

    coordinator.repository.persist_page.assert_awaited_once_with(item_id=item_id, page=page)
    assert events == ["database", "checkpoint"]


@pytest.mark.asyncio
async def test_checkpoint_does_not_advance_when_database_commit_fails() -> None:
    page = OpenCTIPage(items=(_item(),), request_cursor=None, next_cursor="c-1", has_next_page=True)
    item_id = uuid4()
    checkpoint = AsyncMock()
    session = SimpleNamespace(commit=AsyncMock(side_effect=RuntimeError("commit failed")))
    adapter = SimpleNamespace(commit_page=checkpoint)
    coordinator = OpenCTIPersistenceCoordinator(session, adapter)  # type: ignore[arg-type]
    coordinator.repository.persist_page = AsyncMock(return_value=[])  # type: ignore[method-assign]

    with pytest.raises(RuntimeError, match="commit failed"):
        await coordinator.persist_and_checkpoint(item_id=item_id, page=page)

    checkpoint.assert_not_called()
