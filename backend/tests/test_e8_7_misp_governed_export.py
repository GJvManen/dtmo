from __future__ import annotations

from uuid import uuid4

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dtmo.auth.policy import Principal, Role
from dtmo.config import Settings
from dtmo.governance.misp_export import (
    MispExportError,
    deliver_misp_event,
    finalize_misp_export,
    mark_misp_export_uncertain,
    prepare_misp_export,
)
from dtmo.intelligence.model import IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import Base, IntelligenceItem


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _item(
    session: Session,
    *,
    source_id: str = "analyst",
    reviewed: bool = True,
    share_approved: bool = True,
    metadata: dict[str, object] | None = None,
) -> IntelligenceItem:
    item = IntelligenceItem(
        id=uuid4(),
        source_id=source_id,
        external_id=str(uuid4()),
        item_type=IntelligenceType.ADVISORY,
        title="Governed export candidate",
        summary="Bounded intelligence summary",
        canonical_url="https://example.test/intelligence/item",
        content_hash="a" * 64,
        severity=IntelligenceSeverity.MEDIUM,
        confidence_score=80,
        education_relevance=70,
        review_status="reviewed" if reviewed else "candidate",
        share_approved=share_approved,
        metadata_json={
            "reviewed_by": "reviewer@example.test",
            "share_approved_by": "publisher@example.test",
            **(metadata or {}),
        },
    )
    session.add(item)
    session.flush()
    return item


def _publisher() -> Principal:
    return Principal("publisher@example.test", frozenset({Role.PUBLISHER}))


def test_export_feature_flag_is_separate_and_disabled_by_default() -> None:
    settings = Settings(environment="test", feature_misp_connector=True)
    assert settings.feature_misp_connector is True
    assert settings.feature_misp_export is False


def test_export_requires_existing_review_and_share_approval() -> None:
    session = _session()
    item = _item(session, reviewed=False, share_approved=False)

    with pytest.raises(MispExportError, match="review and share approval"):
        prepare_misp_export(
            session,
            item_id=item.id,
            principal=_publisher(),
            request_id="e8-export-unapproved",
            distribution=0,
            sharing_group_id=None,
            tlp="tlp:amber",
        )


def test_service_account_cannot_export_even_if_item_is_approved() -> None:
    session = _session()
    item = _item(session)
    service = Principal("connector:misp", frozenset({Role.SERVICE_ACCOUNT}))

    with pytest.raises(MispExportError, match="service accounts cannot export"):
        prepare_misp_export(
            session,
            item_id=item.id,
            principal=service,
            request_id="e8-export-service",
            distribution=0,
            sharing_group_id=None,
            tlp="tlp:amber",
        )


def test_misp_origin_without_projected_authoritative_restrictions_fails_closed() -> None:
    session = _session()
    item = _item(session, source_id="misp")

    with pytest.raises(MispExportError, match="authoritative source restrictions"):
        prepare_misp_export(
            session,
            item_id=item.id,
            principal=_publisher(),
            request_id="e8-export-misp-origin",
            distribution=0,
            sharing_group_id=None,
            tlp="tlp:red",
        )


def test_authoritative_restrictions_cannot_be_relaxed() -> None:
    session = _session()
    item = _item(
        session,
        source_id="misp",
        metadata={
            "misp_restrictions": {
                "restriction_authoritative": True,
                "distribution": {"value": "1"},
                "sharing_group_id": None,
                "tlp_tags": ["tlp:red"],
            }
        },
    )

    with pytest.raises(MispExportError, match="distribution cannot be changed"):
        prepare_misp_export(
            session,
            item_id=item.id,
            principal=_publisher(),
            request_id="e8-export-relax-distribution",
            distribution=3,
            sharing_group_id=None,
            tlp="tlp:red",
        )

    with pytest.raises(MispExportError, match="less restrictive"):
        prepare_misp_export(
            session,
            item_id=item.id,
            principal=_publisher(),
            request_id="e8-export-relax-tlp",
            distribution=1,
            sharing_group_id=None,
            tlp="tlp:amber",
        )


def test_prepare_finalize_and_revision_replay_block_are_auditable() -> None:
    session = _session()
    item = _item(session)
    publisher = _publisher()

    prepared = prepare_misp_export(
        session,
        item_id=item.id,
        principal=publisher,
        request_id="e8-export-1",
        distribution=0,
        sharing_group_id=None,
        tlp="tlp:amber",
    )
    assert prepared.payload["Event"]["published"] is False
    assert prepared.payload["Event"]["distribution"] == "0"
    assert prepared.payload["Event"]["Tag"] == [{"name": "tlp:amber"}]

    result = finalize_misp_export(
        session,
        prepared=prepared,
        principal=publisher,
        request_id="e8-export-1",
        misp_event_id="42",
    )
    session.commit()
    assert result.misp_event_id == "42"
    assert item.metadata_json["misp_exports"][0]["status"] == "success"

    with pytest.raises(MispExportError, match="replay blocked"):
        prepare_misp_export(
            session,
            item_id=item.id,
            principal=publisher,
            request_id="e8-export-replay",
            distribution=1,
            sharing_group_id=None,
            tlp="tlp:red",
        )


def test_uncertain_delivery_blocks_changed_parameter_replay() -> None:
    session = _session()
    item = _item(session)
    publisher = _publisher()
    prepared = prepare_misp_export(
        session,
        item_id=item.id,
        principal=publisher,
        request_id="e8-export-timeout",
        distribution=0,
        sharing_group_id=None,
        tlp="tlp:amber",
    )
    mark_misp_export_uncertain(
        session,
        prepared=prepared,
        principal=publisher,
        request_id="e8-export-timeout",
    )
    session.commit()

    with pytest.raises(MispExportError, match="replay blocked"):
        prepare_misp_export(
            session,
            item_id=item.id,
            principal=publisher,
            request_id="e8-export-retry",
            distribution=2,
            sharing_group_id=None,
            tlp="tlp:red",
        )


@pytest.mark.asyncio
async def test_delivery_uses_events_add_runtime_secret_and_deterministic_uuid() -> None:
    session = _session()
    item = _item(session)
    prepared = prepare_misp_export(
        session,
        item_id=item.id,
        principal=_publisher(),
        request_id="e8-export-http",
        distribution=0,
        sharing_group_id=None,
        tlp="tlp:amber",
    )
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        seen["authorization"] = request.headers.get("Authorization")
        return httpx.Response(
            200,
            json={"Event": {"id": "42", "uuid": prepared.event_uuid}},
        )

    settings = Settings(
        environment="test",
        misp_api_base="https://misp.example.test",
        misp_api_key="runtime-secret",
        feature_misp_export=True,
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        event_id = await deliver_misp_event(prepared, settings=settings, client=client)

    assert event_id == "42"
    assert seen == {"path": "/events/add", "authorization": "runtime-secret"}
