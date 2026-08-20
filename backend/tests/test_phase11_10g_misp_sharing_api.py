from __future__ import annotations

from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from pydantic import SecretStr

from dtmo.auth.policy import Principal, Role
from dtmo.config import Settings
from dtmo.governance import MispExportError
from dtmo.intelligence.model import IntelligenceSeverity, IntelligenceType
from dtmo.misp_export_api import _validate_runtime_export_settings, export_intelligence_to_misp
from dtmo import misp_export_api
from dtmo.misp_sharing_workspace import (
    _current_event_uuid,
    _safe_exports,
    _safe_restrictions,
    misp_sharing_item_state,
)
from dtmo.persistence.models import IntelligenceItem


class FakeGetSession:
    def __init__(self, item: IntelligenceItem | None) -> None:
        self.item = item

    async def get(self, model: object, item_id: UUID) -> IntelligenceItem | None:
        del model, item_id
        return self.item


class FakeRunSyncSession:
    def __init__(self) -> None:
        self.commits = 0

    async def run_sync(self, fn):  # type: ignore[no-untyped-def]
        return fn(object())

    async def commit(self) -> None:
        self.commits += 1


def _item(
    *,
    source_id: str = "analyst",
    review_status: str = "reviewed",
    share_approved: bool = True,
    metadata: dict[str, object] | None = None,
) -> IntelligenceItem:
    return IntelligenceItem(
        id=uuid4(),
        source_id=source_id,
        external_id=str(uuid4()),
        item_type=IntelligenceType.ADVISORY,
        title="Governed sharing candidate",
        summary="Bounded intelligence summary",
        canonical_url="https://example.invalid/intelligence/item",
        content_hash="a" * 64,
        severity=IntelligenceSeverity.MEDIUM,
        confidence_score=80,
        education_relevance=70,
        review_status=review_status,
        share_approved=share_approved,
        metadata_json={
            "reviewed_by": "reviewer@example.invalid",
            "share_approved_by": "publisher@example.invalid",
            **(metadata or {}),
        },
    )


def _publisher() -> Principal:
    return Principal("publisher@example.invalid", frozenset({Role.PUBLISHER}))


def _valid_settings() -> Settings:
    return Settings(
        environment="test",
        feature_misp_export=True,
        misp_api_base="https://misp.example.invalid",
        misp_api_key="runtime-secret",
    )


def test_sharing_projection_sanitizes_metadata_and_deterministic_identity() -> None:
    item = _item(
        metadata={
            "misp_restrictions": {
                "restriction_authoritative": True,
                "distribution": "1",
                "sharing_group_id": "7",
                "tlp_tags": ["tlp:red", 123, "tlp:amber"],
            },
            "misp_exports": [
                "ignore-me",
                {
                    "status": "success",
                    "event_uuid": "event-1",
                    "misp_event_id": "42",
                    "distribution": 1,
                    "sharing_group_id": "7",
                    "tlp": "tlp:red",
                    "requested_by": "publisher@example.invalid",
                },
            ],
        }
    )

    assert _safe_restrictions(item) == {
        "restriction_authoritative": True,
        "distribution": "1",
        "sharing_group_id": "7",
        "tlp_tags": ["tlp:red", "tlp:amber"],
    }
    assert _safe_exports(item) == [
        {
            "status": "success",
            "event_uuid": "event-1",
            "misp_event_id": "42",
            "distribution": "1",
            "sharing_group_id": "7",
            "tlp": "tlp:red",
            "requested_by": "publisher@example.invalid",
        }
    ]
    assert _current_event_uuid(item) == _current_event_uuid(item)

    item.metadata_json = {"misp_restrictions": "invalid", "misp_exports": {"status": "invalid"}}
    assert _safe_restrictions(item) is None
    assert _safe_exports(item) == []


@pytest.mark.asyncio
async def test_sharing_state_exposes_eligible_canonical_state_without_authority_inference() -> None:
    item = _item()
    state = await misp_sharing_item_state(
        item.id,
        _publisher(),
        FakeGetSession(item),  # type: ignore[arg-type]
        _valid_settings(),
    )

    assert state["export_eligible"] is True
    assert state["export_blockers"] == []
    assert state["reviewed_by"] == "reviewer@example.invalid"
    assert state["share_approved_by"] == "publisher@example.invalid"
    assert state["principal_actions"] == {"can_review": False, "can_approve_share": True}
    assert state["misp_export_enabled"] is True
    assert state["misp_export_configured"] is True
    assert state["runtime_health_claim"] is False
    assert state["publication_authority"] is False
    assert state["synchronization_authority"] is False


@pytest.mark.asyncio
async def test_sharing_state_fails_closed_for_missing_decisions_restrictions_and_replay() -> None:
    candidate = _item(source_id="misp", review_status="candidate", share_approved=False, metadata={})
    candidate.metadata_json = {}
    state = await misp_sharing_item_state(
        candidate.id,
        Principal("service:misp", frozenset({Role.SERVICE_ACCOUNT})),
        FakeGetSession(candidate),  # type: ignore[arg-type]
        Settings(environment="test"),
    )
    assert state["export_eligible"] is False
    assert "independent human review required" in state["export_blockers"]
    assert "separate human share approval required" in state["export_blockers"]
    assert "authoritative MISP source restrictions required before re-export" in state["export_blockers"]
    assert state["principal_actions"] == {"can_review": False, "can_approve_share": False}
    assert state["misp_export_configured"] is False

    reviewed = _item(source_id="misp")
    current_event_uuid = _current_event_uuid(reviewed)
    reviewed.metadata_json = {
        "misp_restrictions": {
            "restriction_authoritative": True,
            "distribution": "0",
            "sharing_group_id": None,
            "tlp_tags": ["tlp:amber"],
        },
        "misp_exports": [{"status": "uncertain", "event_uuid": current_event_uuid}],
    }
    replay_state = await misp_sharing_item_state(
        reviewed.id,
        _publisher(),
        FakeGetSession(reviewed),  # type: ignore[arg-type]
        _valid_settings(),
    )
    assert "review attribution missing" in replay_state["export_blockers"]
    assert "share approval attribution missing" in replay_state["export_blockers"]
    assert "current canonical revision already has uncertain export evidence" in replay_state["export_blockers"]


@pytest.mark.asyncio
async def test_sharing_state_returns_not_found_for_unknown_canonical_item() -> None:
    with pytest.raises(HTTPException) as exc_info:
        await misp_sharing_item_state(
            uuid4(),
            _publisher(),
            FakeGetSession(None),  # type: ignore[arg-type]
            Settings(environment="test"),
        )
    assert exc_info.value.status_code == 404


def test_runtime_export_settings_fail_closed_without_lowering_security_requirements() -> None:
    with pytest.raises(MispExportError, match="feature is disabled"):
        _validate_runtime_export_settings(Settings(environment="test"))
    with pytest.raises(MispExportError, match="configured API base"):
        _validate_runtime_export_settings(Settings(environment="test", feature_misp_export=True))
    with pytest.raises(MispExportError, match="runtime API key"):
        _validate_runtime_export_settings(
            Settings(environment="test", feature_misp_export=True, misp_api_base="https://misp.example.invalid")
        )

    insecure_production = Settings.model_construct(
        environment="production",
        feature_misp_export=True,
        misp_api_base="http://misp.example.invalid",
        misp_api_key=SecretStr("runtime-secret"),
    )
    with pytest.raises(MispExportError, match="requires HTTPS"):
        _validate_runtime_export_settings(insecure_production)

    _validate_runtime_export_settings(_valid_settings())


@pytest.mark.asyncio
async def test_export_api_commits_replay_reservation_and_returns_unpublished_delivery_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    item_id = uuid4()
    audit_event_id = uuid4()
    prepared = object()
    result = SimpleNamespace(
        item_id=item_id,
        replay_key="replay-key",
        event_uuid="event-uuid",
        misp_event_id="42",
        audit_event_id=audit_event_id,
    )
    session = FakeRunSyncSession()

    monkeypatch.setattr(misp_export_api, "prepare_misp_export", lambda *args, **kwargs: prepared)

    async def deliver(*args, **kwargs):  # type: ignore[no-untyped-def]
        return "42"

    monkeypatch.setattr(misp_export_api, "deliver_misp_event", deliver)
    monkeypatch.setattr(misp_export_api, "finalize_misp_export", lambda *args, **kwargs: result)

    response = await export_intelligence_to_misp(
        item_id,
        _publisher(),
        session,  # type: ignore[arg-type]
        _valid_settings(),
        "request-1",
        0,
        None,
        "tlp:amber",
    )

    assert session.commits == 1
    assert response == {
        "id": str(item_id),
        "replay_key": "replay-key",
        "event_uuid": "event-uuid",
        "misp_event_id": "42",
        "audit_event_id": str(audit_event_id),
    }


@pytest.mark.asyncio
async def test_export_api_maps_governance_and_uncertain_delivery_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    item_id = uuid4()
    session = FakeRunSyncSession()

    def blocked(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise MispExportError("replay blocked")

    monkeypatch.setattr(misp_export_api, "prepare_misp_export", blocked)
    with pytest.raises(HTTPException) as conflict:
        await export_intelligence_to_misp(
            item_id,
            _publisher(),
            session,  # type: ignore[arg-type]
            _valid_settings(),
            "request-blocked",
            0,
            None,
            "tlp:amber",
        )
    assert conflict.value.status_code == 409
    assert session.commits == 1

    prepared = object()
    uncertain_calls: list[object] = []
    session = FakeRunSyncSession()
    monkeypatch.setattr(misp_export_api, "prepare_misp_export", lambda *args, **kwargs: prepared)

    async def uncertain_delivery(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise ValueError("invalid MISP response")

    def mark_uncertain(*args, **kwargs):  # type: ignore[no-untyped-def]
        uncertain_calls.append(kwargs["prepared"])

    monkeypatch.setattr(misp_export_api, "deliver_misp_event", uncertain_delivery)
    monkeypatch.setattr(misp_export_api, "mark_misp_export_uncertain", mark_uncertain)

    with pytest.raises(HTTPException) as bad_gateway:
        await export_intelligence_to_misp(
            item_id,
            _publisher(),
            session,  # type: ignore[arg-type]
            _valid_settings(),
            "request-uncertain",
            0,
            None,
            "tlp:amber",
        )
    assert bad_gateway.value.status_code == 502
    assert session.commits == 2
    assert uncertain_calls == [prepared]
