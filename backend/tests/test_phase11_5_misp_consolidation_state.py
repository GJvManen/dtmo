from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from dtmo.persistence.misp import (
    MispSynchronizationState,
    authority_snapshot,
    reconcile_misp_state,
    snapshot_hash,
)


EVENT_UUID = "11111111-2222-4333-8444-555555555555"


def _projection(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "event_uuid": EVENT_UUID,
        "timestamp": "1786737600",
        "distribution": {"value": "4", "label": "sharing-group"},
        "sharing_group_id": "7",
        "tlp_tags": ["tlp:amber+strict"],
        "restriction_authoritative": True,
        "read_only_import": True,
        "external_share_authorized": False,
    }
    value.update(overrides)
    return value


def test_model_enforces_identity_distribution_and_no_share_authority() -> None:
    names = {constraint.name for constraint in MispSynchronizationState.__table__.constraints}
    assert "uq_misp_sync_event_snapshot" in names
    assert "ck_misp_sync_distribution" in names
    assert "ck_misp_sync_sharing_group_required" in names
    assert "ck_misp_sync_no_share_authority" in names
    assert MispSynchronizationState.__table__.c.external_share_authorized.default.arg is False


def test_authority_snapshot_is_stable_and_preserves_restrictions() -> None:
    snapshot = authority_snapshot(_projection())
    assert snapshot["event_uuid"] == EVENT_UUID
    assert snapshot["distribution"] == "4"
    assert snapshot["sharing_group_id"] == "7"
    assert snapshot["tlp_tags"] == ["tlp:amber+strict"]
    assert snapshot["restriction_authoritative"] is True
    assert snapshot["external_share_authorized"] is False
    assert snapshot_hash(snapshot) == snapshot_hash(authority_snapshot(_projection()))


def test_authority_snapshot_fails_closed_on_unknown_or_incomplete_restrictions() -> None:
    with pytest.raises(ValueError, match="known distribution"):
        authority_snapshot(_projection(distribution={"value": "9"}))
    with pytest.raises(ValueError, match="sharing_group_id"):
        authority_snapshot(_projection(sharing_group_id=None))
    with pytest.raises(ValueError, match="not authoritative"):
        authority_snapshot(_projection(restriction_authoritative=False))
    with pytest.raises(ValueError, match="cannot grant external share authority"):
        authority_snapshot(_projection(external_share_authorized=True))


def test_reconcile_projects_authoritative_restrictions_into_canonical_item() -> None:
    item_id = uuid4()
    item = SimpleNamespace(id=item_id, metadata_json={"existing": True})
    session = SimpleNamespace(
        get=Mock(return_value=item),
        scalar=Mock(side_effect=[None, None]),
        add=Mock(),
        flush=Mock(),
    )

    state = reconcile_misp_state(session, item_id=item_id, projection=_projection())  # type: ignore[arg-type]

    assert state.item_id == item_id
    assert state.event_uuid == EVENT_UUID
    assert state.external_share_authorized is False
    assert item.metadata_json["existing"] is True
    assert item.metadata_json["misp_restrictions"]["distribution"] == "4"
    assert item.metadata_json["misp_restrictions"]["sharing_group_id"] == "7"
    session.add.assert_called_once_with(state)
    session.flush.assert_called_once()


def test_reconcile_fails_closed_on_event_identity_collision() -> None:
    item_id = uuid4()
    other_item_id = uuid4()
    item = SimpleNamespace(id=item_id, metadata_json={})
    existing = SimpleNamespace(item_id=other_item_id, event_uuid=EVENT_UUID)
    session = SimpleNamespace(
        get=Mock(return_value=item),
        scalar=Mock(side_effect=[None, existing]),
        add=Mock(),
        flush=Mock(),
    )

    with pytest.raises(ValueError, match="already mapped"):
        reconcile_misp_state(session, item_id=item_id, projection=_projection())  # type: ignore[arg-type]

    session.add.assert_not_called()
