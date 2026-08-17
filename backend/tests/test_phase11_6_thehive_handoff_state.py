from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi.routing import APIRoute

from dtmo.auth.policy import Permission, Principal, Role
from dtmo.integrations.thehive import TheHiveCaseResult, TheHivePolicyError
from dtmo.persistence.thehive import TheHiveHandoffRepository, TheHiveHandoffState
from dtmo.thehive_handoff import router, validate_authoritative_handling


def test_case_handoff_permission_is_human_only_and_distinct_from_share_approval() -> None:
    cert = Principal(subject="cert-human", roles=frozenset({Role.CERT}))
    service = Principal(subject="svc", roles=frozenset({Role.SERVICE_ACCOUNT}))
    publisher = Principal(subject="publisher", roles=frozenset({Role.PUBLISHER}))

    assert cert.can(Permission.CASE_HANDOFF)
    assert not service.can(Permission.CASE_HANDOFF)
    assert not publisher.can(Permission.CASE_HANDOFF)
    assert Permission.CASE_HANDOFF is not Permission.SHARE_APPROVE


def test_thehive_state_enforces_no_share_and_no_compromise_authority() -> None:
    names = {constraint.name for constraint in TheHiveHandoffState.__table__.constraints}
    assert "uq_thehive_handoff_request" in names
    assert "uq_thehive_handoff_case" in names
    assert "ck_thehive_handoff_status" in names
    assert "ck_thehive_handoff_no_share_authority" in names
    assert "ck_thehive_handoff_no_compromise_proof" in names
    assert TheHiveHandoffState.__table__.c.external_share_authorized.default.arg is False
    assert TheHiveHandoffState.__table__.c.local_compromise_proven.default.arg is False


def test_thehive_routes_are_bounded_to_handoff_and_history() -> None:
    routes = {
        (route.path, tuple(sorted(route.methods or set())))
        for route in router.routes
        if isinstance(route, APIRoute)
    }
    assert ("/api/v1/thehive/items/{item_id}/cases", ("POST",)) in routes
    assert ("/api/v1/thehive/items/{item_id}/handoffs", ("GET",)) in routes


def test_authoritative_tlp_cannot_be_broadened_and_misp_access_ambiguity_blocks_handoff() -> None:
    item = SimpleNamespace(tags=["tlp:red"], metadata_json={})
    with pytest.raises(TheHivePolicyError, match="broaden"):
        validate_authoritative_handling(item, "amber")  # type: ignore[arg-type]

    misp_item = SimpleNamespace(
        tags=["tlp:amber"],
        metadata_json={
            "misp_restrictions": {
                "restriction_authoritative": True,
                "distribution": "4",
                "sharing_group_id": "7",
            }
        },
    )
    with pytest.raises(TheHivePolicyError, match="MISP distribution/sharing-group"):
        validate_authoritative_handling(misp_item, "amber")  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_reservation_is_committed_before_any_external_mutation_can_run() -> None:
    item_id = uuid4()
    request_id = uuid4()
    state = SimpleNamespace(
        id=uuid4(),
        request_id=request_id,
        item_id=item_id,
        requested_by="cert-human",
        organization="school-cert",
        status="reserved",
    )
    session = SimpleNamespace(
        get=AsyncMock(return_value=SimpleNamespace(id=item_id)),
        scalar=AsyncMock(return_value=None),
        add=Mock(),
        commit=AsyncMock(),
        refresh=AsyncMock(side_effect=lambda obj: obj.__dict__.update(state.__dict__)),
    )
    repository = TheHiveHandoffRepository(session)  # type: ignore[arg-type]

    result = await repository.reserve(
        request_id=request_id,
        item_id=item_id,
        requested_by="cert-human",
        organization="school-cert",
        tlp="amber",
        pap="amber",
        authority_snapshot={"human_authorized": True},
    )

    assert result.status == "reserved"
    session.add.assert_called_once()
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delivered_state_persists_only_minimized_identity_outcome() -> None:
    state = SimpleNamespace(
        status="reserved",
        thehive_case_id=None,
        thehive_case_number=None,
        outcome={},
        error_detail=None,
        updated_at=None,
    )
    session = SimpleNamespace(commit=AsyncMock(), refresh=AsyncMock())
    repository = TheHiveHandoffRepository(session)  # type: ignore[arg-type]
    result = TheHiveCaseResult(
        case_id="case-1",
        case_number=42,
        organization="school-cert",
        raw_result={"_id": "case-1", "number": 42, "sensitive": "must-not-persist"},
    )

    await repository.mark_delivered(state, result)  # type: ignore[arg-type]

    assert state.outcome == {
        "case_id": "case-1",
        "case_number": 42,
        "organization": "school-cert",
    }
    assert "sensitive" not in state.outcome


@pytest.mark.asyncio
async def test_ambiguous_or_delivered_request_cannot_be_blindly_replayed() -> None:
    item_id = uuid4()
    request_id = uuid4()
    existing = SimpleNamespace(
        request_id=request_id,
        item_id=item_id,
        requested_by="cert-human",
        organization="school-cert",
        status="ambiguous",
    )
    session = SimpleNamespace(
        get=AsyncMock(return_value=SimpleNamespace(id=item_id)),
        scalar=AsyncMock(return_value=existing),
        add=Mock(),
        commit=AsyncMock(),
        refresh=AsyncMock(),
    )
    repository = TheHiveHandoffRepository(session)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="reconciliation required"):
        await repository.reserve(
            request_id=request_id,
            item_id=item_id,
            requested_by="cert-human",
            organization="school-cert",
            tlp="amber",
            pap="amber",
            authority_snapshot={"human_authorized": True},
        )

    session.add.assert_not_called()
    session.commit.assert_not_awaited()
