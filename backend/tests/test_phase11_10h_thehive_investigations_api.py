from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException

from dtmo import thehive_handoff
from dtmo.auth.policy import Principal, Role
from dtmo.config import Settings
from dtmo.intelligence.model import IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.thehive import TheHiveHandoffState
from dtmo.thehive_handoff import investigation_state


class FakeSession:
    def __init__(self, item: IntelligenceItem | None, provenance_count: int) -> None:
        self.item = item
        self.provenance_count = provenance_count

    async def get(self, model: object, item_id):  # type: ignore[no-untyped-def]
        del model, item_id
        return self.item

    async def scalar(self, statement):  # type: ignore[no-untyped-def]
        del statement
        return self.provenance_count


class FakeRepository:
    records: list[TheHiveHandoffState] = []

    def __init__(self, session: object) -> None:
        del session

    async def list_for_item(self, item_id):  # type: ignore[no-untyped-def]
        del item_id
        return list(self.records)


def make_item(*, metadata: dict[str, object] | None = None) -> IntelligenceItem:
    return IntelligenceItem(
        id=uuid4(),
        source_id="analyst",
        external_id=str(uuid4()),
        item_type=IntelligenceType.ADVISORY,
        title="Investigate suspicious education-sector activity",
        summary="Canonical evidence summary",
        canonical_url="https://example.invalid/intelligence/investigation",
        content_hash="b" * 64,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=85,
        education_relevance=90,
        review_status="reviewed",
        share_approved=False,
        tags=["tlp:amber", "education"],
        metadata_json=metadata or {},
    )


def handoff(item: IntelligenceItem, *, status: str = "delivered") -> TheHiveHandoffState:
    now = datetime.now(UTC)
    return TheHiveHandoffState(
        id=uuid4(),
        request_id=uuid4(),
        item_id=item.id,
        requested_by="analyst@example.invalid",
        organization="school-cert",
        tlp="amber",
        pap="amber",
        authority_snapshot={"human_authorized": True},
        status=status,
        thehive_case_id="case-42" if status == "delivered" else None,
        thehive_case_number="42" if status == "delivered" else None,
        outcome={},
        error_detail="manual reconciliation required" if status == "ambiguous" else None,
        created_at=now,
        updated_at=now,
        external_share_authorized=False,
        local_compromise_proven=False,
    )


def enabled_settings() -> Settings:
    return Settings(
        environment="test",
        feature_thehive_handoff=True,
        thehive_api_base="https://thehive.example.invalid",
        thehive_api_token="runtime-token",
        thehive_organization="school-cert",
    )


@pytest.mark.asyncio
async def test_investigation_state_projects_canonical_handoff_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    item = make_item()
    FakeRepository.records = [handoff(item)]
    monkeypatch.setattr(thehive_handoff, "TheHiveHandoffRepository", FakeRepository)

    result = await investigation_state(
        item.id,
        Principal("analyst@example.invalid", frozenset({Role.SENIOR_ANALYST})),
        FakeSession(item, 2),  # type: ignore[arg-type]
        enabled_settings(),
    )

    assert result.item_id == item.id
    assert result.provenance_count == 2
    assert result.authoritative_tlp_tags == ["tlp:amber"]
    assert result.principal_actions == {"can_handoff": True}
    assert result.feature_enabled is True
    assert result.configured is True
    assert result.handoff_blockers == []
    assert result.runtime_health_claim is False
    assert result.upstream_case_readback_supported is False
    assert result.alerts_tasks_timeline_persisted is False
    assert result.external_share_authority is False
    assert result.local_compromise_proof is False
    assert len(result.handoff_history) == 1
    assert result.handoff_history[0].thehive_case_id == "case-42"
    assert result.handoff_history[0].external_share_authorized is False
    assert result.handoff_history[0].local_compromise_proven is False


@pytest.mark.asyncio
async def test_investigation_state_fails_closed_on_missing_prerequisites_and_misp_mapping(monkeypatch: pytest.MonkeyPatch) -> None:
    item = make_item(
        metadata={
            "misp_restrictions": {
                "restriction_authoritative": True,
                "distribution": "0",
                "sharing_group_id": None,
            }
        }
    )
    FakeRepository.records = [handoff(item, status="ambiguous")]
    monkeypatch.setattr(thehive_handoff, "TheHiveHandoffRepository", FakeRepository)

    result = await investigation_state(
        item.id,
        Principal("service:thehive", frozenset({Role.SERVICE_ACCOUNT})),
        FakeSession(item, 0),  # type: ignore[arg-type]
        Settings(environment="test"),
    )

    assert result.principal_actions == {"can_handoff": False}
    assert result.feature_enabled is False
    assert result.configured is False
    assert "canonical provenance required before TheHive case handoff" in result.handoff_blockers
    assert "TheHive case handoff feature is disabled" in result.handoff_blockers
    assert "TheHive case handoff runtime configuration is incomplete" in result.handoff_blockers
    assert "current principal lacks human case-handoff authority" in result.handoff_blockers
    assert any("authoritative MISP" in blocker for blocker in result.handoff_blockers)
    assert result.handoff_history[0].status == "ambiguous"
    assert result.handoff_history[0].error_detail == "manual reconciliation required"


@pytest.mark.asyncio
async def test_investigation_state_returns_not_found_for_unknown_item(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeRepository.records = []
    monkeypatch.setattr(thehive_handoff, "TheHiveHandoffRepository", FakeRepository)

    with pytest.raises(HTTPException) as exc_info:
        await investigation_state(
            uuid4(),
            Principal("reader@example.invalid", frozenset({Role.ANALYST})),
            FakeSession(None, 0),  # type: ignore[arg-type]
            Settings(environment="test"),
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "canonical intelligence item not found"
