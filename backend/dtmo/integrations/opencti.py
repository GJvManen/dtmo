from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from dtmo.config import Settings


OPENCTI_STIX_CORE_OBJECTS_QUERY = """
query DtmoOpenCTIRead($first: Int!, $after: ID) {
  stixCoreObjects(first: $first, after: $after) {
    edges {
      node {
        id
        standard_id
        entity_type
        parent_types
        created_at
        updated_at
        confidence
        objectMarking {
          edges { node { id definition_type definition } }
        }
        externalReferences {
          edges { node { id source_name url external_id description } }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
""".strip()


@dataclass(slots=True, frozen=True)
class OpenCTIItem:
    opencti_id: str
    stix_id: str
    entity_type: str
    parent_types: tuple[str, ...]
    markings: tuple[dict[str, str], ...]
    confidence: int | None
    created_at: str | None
    updated_at: str | None
    external_references: tuple[dict[str, Any], ...]
    provenance: dict[str, Any]


@dataclass(slots=True, frozen=True)
class OpenCTIPage:
    items: tuple[OpenCTIItem, ...]
    request_cursor: str | None
    next_cursor: str | None
    has_next_page: bool


class OpenCTIPolicyError(ValueError):
    pass


class OpenCTICheckpointStore:
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load_cursor(self) -> str | None:
        if not self.path.exists():
            return None
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise OpenCTIPolicyError("OpenCTI checkpoint is unreadable or malformed") from exc
        if not isinstance(payload, dict):
            raise OpenCTIPolicyError("OpenCTI checkpoint must be an object")
        cursor = payload.get("cursor")
        if cursor is None:
            return None
        if not isinstance(cursor, str) or not cursor.strip():
            raise OpenCTIPolicyError("OpenCTI checkpoint cursor is invalid")
        return cursor.strip()

    def commit(self, page: OpenCTIPage) -> None:
        if page.has_next_page and not page.next_cursor:
            raise OpenCTIPolicyError("OpenCTI page cannot advance without a next cursor")
        cursor = page.next_cursor if page.has_next_page else None
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        temporary.write_text(
            json.dumps({"cursor": cursor, "completed": not page.has_next_page}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, self.path)


class OpenCTIReadAdapter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.checkpoints = OpenCTICheckpointStore(settings.opencti_checkpoint_path)

    def _headers(self) -> dict[str, str]:
        token = self.settings.opencti_api_token.get_secret_value().strip()
        if not token:
            raise OpenCTIPolicyError("OpenCTI API token is required")
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    @staticmethod
    def _connection(payload: Any) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise OpenCTIPolicyError("OpenCTI response must be an object")
        errors = payload.get("errors")
        if errors:
            raise OpenCTIPolicyError("OpenCTI GraphQL response contains errors")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise OpenCTIPolicyError("OpenCTI response has no data object")
        connection = data.get("stixCoreObjects")
        if not isinstance(connection, dict):
            raise OpenCTIPolicyError("OpenCTI response has no STIX object connection")
        return connection

    @staticmethod
    def _edge_nodes(value: Any, field: str) -> list[dict[str, Any]]:
        if not isinstance(value, dict):
            raise OpenCTIPolicyError(f"OpenCTI {field} connection is malformed")
        edges = value.get("edges", [])
        if not isinstance(edges, list):
            raise OpenCTIPolicyError(f"OpenCTI {field} edges must be a list")
        nodes: list[dict[str, Any]] = []
        for edge in edges:
            if not isinstance(edge, dict) or not isinstance(edge.get("node"), dict):
                raise OpenCTIPolicyError(f"OpenCTI {field} edge is malformed")
            nodes.append(edge["node"])
        return nodes

    def _normalize_node(self, node: Any) -> OpenCTIItem:
        if not isinstance(node, dict):
            raise OpenCTIPolicyError("OpenCTI STIX node must be an object")
        opencti_id = str(node.get("id", "")).strip()
        stix_id = str(node.get("standard_id", "")).strip()
        entity_type = str(node.get("entity_type", "")).strip()
        if not opencti_id or not stix_id or not entity_type:
            raise OpenCTIPolicyError("OpenCTI STIX node is missing stable identity or type")

        allowed = {part.strip().lower() for part in self.settings.opencti_allowed_entity_types.split(",") if part.strip()}
        if allowed and entity_type.lower() not in allowed:
            raise OpenCTIPolicyError(f"OpenCTI entity type is outside the explicit allowlist: {entity_type}")

        parent_types_raw = node.get("parent_types", [])
        if not isinstance(parent_types_raw, list) or not all(isinstance(value, str) for value in parent_types_raw):
            raise OpenCTIPolicyError("OpenCTI parent_types is malformed")

        markings_raw = self._edge_nodes(node.get("objectMarking", {"edges": []}), "marking")
        markings: list[dict[str, str]] = []
        for marking in markings_raw:
            marking_id = str(marking.get("id", "")).strip()
            definition_type = str(marking.get("definition_type", "")).strip()
            definition = str(marking.get("definition", "")).strip()
            if not marking_id or not definition_type or not definition:
                raise OpenCTIPolicyError("OpenCTI marking is missing identity or definition")
            markings.append({"id": marking_id, "definition_type": definition_type, "definition": definition})

        references = tuple(dict(item) for item in self._edge_nodes(node.get("externalReferences", {"edges": []}), "external reference"))
        confidence_raw = node.get("confidence")
        if confidence_raw is not None and (not isinstance(confidence_raw, int) or isinstance(confidence_raw, bool) or confidence_raw < 0 or confidence_raw > 100):
            raise OpenCTIPolicyError("OpenCTI confidence must be an integer between 0 and 100")

        return OpenCTIItem(
            opencti_id=opencti_id,
            stix_id=stix_id,
            entity_type=entity_type,
            parent_types=tuple(parent_types_raw),
            markings=tuple(markings),
            confidence=confidence_raw,
            created_at=str(node["created_at"]) if node.get("created_at") is not None else None,
            updated_at=str(node["updated_at"]) if node.get("updated_at") is not None else None,
            external_references=references,
            provenance={
                "system": "OpenCTI",
                "boundary": "GraphQL/stixCoreObjects",
                "opencti_id": opencti_id,
                "stix_id": stix_id,
                "read_only": True,
                "external_share_authorized": False,
                "local_compromise_proven": False,
            },
        )

    async def read_pages(self, client: httpx.AsyncClient) -> list[OpenCTIPage]:
        base = self.settings.opencti_api_base.rstrip("/")
        if not base:
            raise OpenCTIPolicyError("OpenCTI API base is required")
        cursor = self.checkpoints.load_cursor()
        pages: list[OpenCTIPage] = []
        for _ in range(self.settings.opencti_max_pages):
            response = await client.post(
                f"{base}/graphql",
                headers=self._headers(),
                json={"query": OPENCTI_STIX_CORE_OBJECTS_QUERY, "variables": {"first": self.settings.opencti_page_size, "after": cursor}},
            )
            response.raise_for_status()
            connection = self._connection(response.json())
            edges = connection.get("edges")
            page_info = connection.get("pageInfo")
            if not isinstance(edges, list) or not isinstance(page_info, dict):
                raise OpenCTIPolicyError("OpenCTI page structure is malformed")
            items: list[OpenCTIItem] = []
            for edge in edges:
                if not isinstance(edge, dict):
                    raise OpenCTIPolicyError("OpenCTI STIX edge is malformed")
                items.append(self._normalize_node(edge.get("node")))
            has_next = page_info.get("hasNextPage")
            next_cursor = page_info.get("endCursor")
            if not isinstance(has_next, bool):
                raise OpenCTIPolicyError("OpenCTI pageInfo.hasNextPage is malformed")
            if has_next and (not isinstance(next_cursor, str) or not next_cursor.strip()):
                raise OpenCTIPolicyError("OpenCTI next page is missing a cursor")
            normalized_cursor = next_cursor.strip() if isinstance(next_cursor, str) and next_cursor.strip() else None
            page = OpenCTIPage(tuple(items), cursor, normalized_cursor, has_next)
            pages.append(page)
            if not has_next:
                break
            cursor = normalized_cursor
        return pages

    def commit_page(self, page: OpenCTIPage) -> None:
        """Advance durable state only after the caller has persisted the page successfully."""
        self.checkpoints.commit(page)
