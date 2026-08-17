from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest

from dtmo.integrations.thehive import (
    TheHiveAmbiguousDelivery,
    TheHiveCaseAdapter,
    TheHivePolicyError,
    build_case_payload,
)


def test_payload_mapping_is_minimized_deterministic_and_fail_closed() -> None:
    payload = build_case_payload(
        canonical_id="11111111-1111-1111-1111-111111111111",
        title="  Important   incident  ",
        summary="Reviewed summary only",
        severity="high",
        tlp="amber+strict",
        pap="amber",
        tags=["education", "education", "  cve  ", ""],
    )

    assert payload == {
        "title": "Important incident",
        "description": "Reviewed summary only\n\nDTMO canonical reference: 11111111-1111-1111-1111-111111111111",
        "severity": 3,
        "tlp": 4,
        "pap": 2,
        "tags": ["cve", "education"],
    }

    with pytest.raises(TheHivePolicyError, match="unknown TLP"):
        build_case_payload(
            canonical_id="id",
            title="title",
            summary="summary",
            severity="medium",
            tlp="unknown",
            pap="amber",
            tags=[],
        )


@pytest.mark.asyncio
async def test_adapter_accepts_only_confirmed_stable_case_identity() -> None:
    adapter = TheHiveCaseAdapter(api_base="https://thehive.example", api_token="secret", organization="school-cert")
    request = httpx.Request("POST", "https://thehive.example/api/v1/case")
    response = httpx.Response(201, request=request, json={"_id": "case-1", "number": 42})
    client = AsyncMock(spec=httpx.AsyncClient)
    client.post.return_value = response

    result = await adapter.create_case(client, {"title": "x"})

    assert result.case_id == "case-1"
    assert result.case_number == 42
    _, kwargs = client.post.call_args
    assert kwargs["headers"]["X-Organisation"] == "school-cert"
    assert kwargs["headers"]["Authorization"] == "Bearer secret"


@pytest.mark.asyncio
async def test_adapter_marks_success_without_identity_as_ambiguous() -> None:
    adapter = TheHiveCaseAdapter(api_base="https://thehive.example", api_token="secret", organization="school-cert")
    request = httpx.Request("POST", "https://thehive.example/api/v1/case")
    client = AsyncMock(spec=httpx.AsyncClient)
    client.post.return_value = httpx.Response(201, request=request, json={"number": 42})

    with pytest.raises(TheHiveAmbiguousDelivery, match="stable case identity"):
        await adapter.create_case(client, {"title": "x"})
