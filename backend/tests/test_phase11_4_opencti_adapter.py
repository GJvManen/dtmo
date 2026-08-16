from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from pydantic import SecretStr

from dtmo.config import Settings
from dtmo.integrations.opencti import OpenCTIPage, OpenCTIPolicyError, OpenCTIReadAdapter


pytestmark = pytest.mark.asyncio


def _settings(tmp_path: Path, **overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "opencti_api_base": "https://opencti.example",
        "opencti_api_token": SecretStr("test-token"),
        "opencti_page_size": 2,
        "opencti_max_pages": 3,
        "opencti_allowed_entity_types": "indicator,vulnerability",
        "opencti_checkpoint_path": str(tmp_path / "opencti.json"),
    }
    values.update(overrides)
    return Settings(**values)


def _node(identifier: str, standard_id: str, entity_type: str = "Indicator") -> dict[str, object]:
    return {
        "id": identifier,
        "standard_id": standard_id,
        "entity_type": entity_type,
        "parent_types": ["Stix-Core-Object"],
        "created_at": "2026-08-16T12:00:00Z",
        "updated_at": "2026-08-16T12:10:00Z",
        "confidence": 80,
        "objectMarking": {
            "edges": [
                {
                    "node": {
                        "id": "marking--amber",
                        "definition_type": "TLP",
                        "definition": "TLP:AMBER",
                    }
                }
            ]
        },
        "externalReferences": {
            "edges": [
                {
                    "node": {
                        "id": "external-reference--1",
                        "source_name": "source-a",
                        "url": "https://example.test/reference",
                        "external_id": "REF-1",
                        "description": "attributed source",
                    }
                }
            ]
        },
    }


def _payload(nodes: list[dict[str, object]], *, has_next: bool, cursor: str | None) -> dict[str, object]:
    return {
        "data": {
            "stixCoreObjects": {
                "edges": [{"node": node} for node in nodes],
                "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
            }
        }
    }


async def test_opencti_adapter_reads_bounded_pages_and_preserves_provenance(tmp_path: Path) -> None:
    requests: list[dict[str, object]] = []
    responses = [
        _payload([_node("o-1", "indicator--1")], has_next=True, cursor="cursor-1"),
        _payload([_node("o-2", "vulnerability--2", "Vulnerability")], has_next=False, cursor=None),
    ]

    async def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        requests.append(body)
        return httpx.Response(200, json=responses[len(requests) - 1])

    adapter = OpenCTIReadAdapter(_settings(tmp_path))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        pages = await adapter.read_pages(client)

    assert len(pages) == 2
    assert requests[0]["variables"] == {"first": 2, "after": None}
    assert requests[1]["variables"] == {"first": 2, "after": "cursor-1"}
    first = pages[0].items[0]
    assert first.opencti_id == "o-1"
    assert first.stix_id == "indicator--1"
    assert first.markings[0]["definition"] == "TLP:AMBER"
    assert first.provenance["read_only"] is True
    assert first.provenance["external_share_authorized"] is False
    assert first.provenance["local_compromise_proven"] is False
    assert not Path(adapter.settings.opencti_checkpoint_path).exists()


async def test_checkpoint_advances_only_after_explicit_persistence_commit(tmp_path: Path) -> None:
    adapter = OpenCTIReadAdapter(_settings(tmp_path))
    page = OpenCTIPage(items=(), request_cursor=None, next_cursor="cursor-1", has_next_page=True)
    checkpoint = Path(adapter.settings.opencti_checkpoint_path)

    assert not checkpoint.exists()
    adapter.commit_page(page)
    assert json.loads(checkpoint.read_text(encoding="utf-8")) == {"completed": False, "cursor": "cursor-1"}

    restarted = OpenCTIReadAdapter(_settings(tmp_path))
    seen_after: list[str | None] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen_after.append(json.loads(request.content)["variables"]["after"])
        return httpx.Response(200, json=_payload([], has_next=False, cursor=None))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await restarted.read_pages(client)
    assert seen_after == ["cursor-1"]


@pytest.mark.parametrize(
    "payload",
    [
        {"errors": [{"message": "forbidden"}]},
        {"data": {"stixCoreObjects": {"edges": [], "pageInfo": {"hasNextPage": True, "endCursor": None}}}},
        _payload([{"id": "o-1", "standard_id": "indicator--1", "entity_type": "Indicator", "parent_types": [], "objectMarking": {"edges": [{"node": {"id": "m-1"}}]}, "externalReferences": {"edges": []}}], has_next=False, cursor=None),
        _payload([_node("o-1", "indicator--1", "Report")], has_next=False, cursor=None),
    ],
)
async def test_opencti_adapter_fails_closed_without_checkpoint_advance(tmp_path: Path, payload: dict[str, object]) -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    adapter = OpenCTIReadAdapter(_settings(tmp_path))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(OpenCTIPolicyError):
            await adapter.read_pages(client)
    assert not Path(adapter.settings.opencti_checkpoint_path).exists()


async def test_opencti_adapter_enforces_max_pages(tmp_path: Path) -> None:
    count = 0

    async def handler(_: httpx.Request) -> httpx.Response:
        nonlocal count
        count += 1
        return httpx.Response(200, json=_payload([_node(f"o-{count}", f"indicator--{count}")], has_next=True, cursor=f"cursor-{count}"))

    adapter = OpenCTIReadAdapter(_settings(tmp_path, opencti_max_pages=2))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        pages = await adapter.read_pages(client)
    assert len(pages) == 2
    assert count == 2


def test_production_opencti_read_requires_https_token_allowlist_and_durable_path() -> None:
    common = {
        "environment": "production",
        "minio_secure": True,
        "minio_secret_key": SecretStr("object-secret"),
        "jwt_jwks_json": SecretStr('{"keys":[{"kty":"RSA","kid":"1","n":"abc","e":"AQAB"}]}'),
        "privacy_pseudonymization_secret": SecretStr("x" * 32),
        "feature_opencti_read": True,
    }
    with pytest.raises(ValueError, match="HTTPS API base"):
        Settings(**common, opencti_api_base="http://opencti", opencti_api_token=SecretStr("token"))
    with pytest.raises(ValueError, match="runtime API token"):
        Settings(**common, opencti_api_base="https://opencti", opencti_api_token=SecretStr(""))
    with pytest.raises(ValueError, match="entity-type allowlist"):
        Settings(**common, opencti_api_base="https://opencti", opencti_api_token=SecretStr("token"), opencti_allowed_entity_types="")
    with pytest.raises(ValueError, match="absolute durable checkpoint path"):
        Settings(**common, opencti_api_base="https://opencti", opencti_api_token=SecretStr("token"), opencti_checkpoint_path="relative.json")
