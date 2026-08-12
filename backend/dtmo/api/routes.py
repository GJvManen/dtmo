from __future__ import annotations

import json
import re
from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.auth.revocation import revoke_token_with_audit
from dtmo.auth.token_state import TokenStateError, TokenStateStore
from dtmo.config import Settings, get_settings
from dtmo.connectors.base import ConnectorRecord
from dtmo.governance import (
    GovernedDecisionError,
    approve_intelligence_sharing,
    review_intelligence,
)
from dtmo.intelligence import IntelligenceType
from dtmo.lake.minio_store import MinioObjectStore
from dtmo.lake.service import IntelligenceLake
from dtmo.persistence.repository import IntelligenceRepository
from dtmo.persistence.session import Database
from dtmo.search.service import OpenSearchService

from .schemas import (
    IntelligenceIngestRequest,
    IntelligenceIngestResponse,
    SearchResponse,
    TokenRevocationRequest,
    TokenRevocationResponse,
)

router = APIRouter(prefix="/api/v1", tags=["intelligence"])
database = Database()
lake = IntelligenceLake(MinioObjectStore())
search_service = OpenSearchService()

_CONNECTOR_ITEM_TYPE_ALIASES = {
    "security-advisory": IntelligenceType.ADVISORY.value,
}
_CVE_ID = re.compile(r"^CVE-\d{4}-\d{4,7}$", re.IGNORECASE)


def _normalize_connector_item_type(value: str) -> str:
    """Normalize a bounded connector alias to the canonical intelligence enum."""

    candidate = value.strip().lower()
    candidate = _CONNECTOR_ITEM_TYPE_ALIASES.get(candidate, candidate)
    try:
        return IntelligenceType(candidate).value
    except ValueError as exc:
        raise ValueError(f"unsupported connector item type: {value}") from exc


def _canonical_connector_url(connector_id: str, record: ConnectorRecord) -> str:
    """Return a canonical HTTP(S) URL without weakening the ingest URL policy.

    NVD CVE records can contain non-HTTP(S) vendor references (including FTP) in
    their raw upstream payload. Those references remain preserved in raw evidence,
    while the canonical/provenance URL is the stable NVD HTTPS detail page.
    """

    if connector_id == "nvd-cve" and _CVE_ID.fullmatch(record.external_id):
        return f"https://nvd.nist.gov/vuln/detail/{record.external_id.upper()}"
    return record.url


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in database.session():
        yield session


async def _persist_intelligence(
    request: IntelligenceIngestRequest,
    *,
    actor_subject: str,
    session: AsyncSession,
) -> IntelligenceIngestResponse:
    raw = json.dumps(request.raw_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    external_id = request.external_id or request.title
    receipt = await lake.land(
        source_id=request.source_id,
        external_id=external_id,
        payload=raw,
        content_type="application/json",
    )
    repository = IntelligenceRepository(session)
    payload = request.model_dump(mode="python", exclude={"raw_payload"})
    payload["canonical_url"] = str(request.canonical_url)
    payload["content_hash"] = receipt.sha256
    payload["metadata"] = {
        **request.metadata,
        "raw_object": {
            "bucket": receipt.bucket,
            "key": receipt.key,
            "sha256": receipt.sha256,
            "size": receipt.size,
        },
        "ingested_by": actor_subject,
    }
    payload["provenance"] = [
        {
            **entry.model_dump(mode="python"),
            "source_url": str(entry.source_url),
            "content_hash": receipt.sha256,
        }
        for entry in request.provenance
    ]
    item, inserted = await repository.ingest_candidate(payload)

    # PUT-by-ID in OpenSearch is idempotent. Always attempt indexing so that an
    # operator can replay a connector after a previous index outage or mapping
    # failure and repair search without duplicating the canonical DB record.
    indexed = False
    try:
        await search_service.index_document(
            str(item.id),
            {
                "title": item.title,
                "summary": item.summary,
                "item_type": item.item_type,
                "source_id": item.source_id,
                "severity": item.severity,
                "confidence_score": item.confidence_score,
                "confidence_level": item.confidence_level,
                "confidence_rationale": item.confidence_rationale,
                "education_relevance": item.education_relevance,
                "published_at": item.published_at.isoformat() if item.published_at else None,
                "canonical_url": item.canonical_url,
                "tags": item.tags,
            },
        )
        indexed = True
        if item.metadata_json.get("search_index_status") == "failed":
            item.metadata_json = {
                key: value
                for key, value in item.metadata_json.items()
                if key not in {"search_index_status", "search_index_error"}
            }
    except Exception as exc:
        item.metadata_json = {
            **item.metadata_json,
            "search_index_status": "failed",
            "search_index_error": type(exc).__name__,
        }

    return IntelligenceIngestResponse(
        id=str(item.id),
        inserted=inserted,
        review_status=item.review_status,
        share_approved=item.share_approved,
        raw_object_key=receipt.key,
        raw_sha256=receipt.sha256,
        indexed=indexed,
    )


async def ingest_connector_record(connector_id: str, record: ConnectorRecord) -> IntelligenceIngestResponse:
    """Land, canonicalize, commit and index one trusted connector record.

    Connector execution is a service ingestion path, never a human publication path.
    Review and external share approval remain separate governed human decisions.
    A connector receipt is returned only after the canonical database session has
    resumed past its yield and committed successfully.
    """

    canonical_item_type = _normalize_connector_item_type(record.object_type)
    canonical_url = _canonical_connector_url(connector_id, record)
    request = IntelligenceIngestRequest.model_validate(
        {
            "source_id": connector_id,
            "external_id": record.external_id,
            "item_type": canonical_item_type,
            "title": record.title,
            "summary": record.summary,
            "canonical_url": canonical_url,
            "published_at": record.published_at,
            "severity": "informational",
            "confidence": record.confidence,
            "education_relevance": 80,
            "tags": [record.external_id, canonical_item_type, connector_id],
            "metadata": {
                "source_reliability": record.source_reliability,
                "connector_managed": True,
                "connector_object_type": record.object_type,
            },
            "provenance": [
                {
                    "source_url": canonical_url,
                    "source_title": record.title,
                    "publisher": connector_id,
                    "confidence": record.confidence,
                }
            ],
            "raw_payload": record.raw,
        }
    )
    persisted: IntelligenceIngestResponse | None = None
    async for session in database.session():
        persisted = await _persist_intelligence(
            request,
            actor_subject=f"connector:{connector_id}",
            session=session,
        )
    if persisted is not None:
        return persisted
    raise RuntimeError("database session unavailable")


@router.post(
    "/intelligence",
    response_model=IntelligenceIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_intelligence(
    request: IntelligenceIngestRequest,
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.INGEST_INTELLIGENCE)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IntelligenceIngestResponse:
    return await _persist_intelligence(
        request,
        actor_subject=principal.subject,
        session=session,
    )


@router.post("/intelligence/{item_id}/review")
async def review_intelligence_item(
    item_id: UUID,
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.REVIEW_INTELLIGENCE)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> dict[str, str | bool]:
    try:
        result = await session.run_sync(
            lambda sync_session: review_intelligence(
                sync_session,
                item_id=item_id,
                principal=principal,
                request_id=request_id,
            )
        )
    except GovernedDecisionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {
        "id": str(result.item_id),
        "review_status": result.review_status,
        "share_approved": result.share_approved,
        "audit_event_id": str(result.audit_event_id),
    }


@router.post("/intelligence/{item_id}/share-approval")
async def approve_intelligence_item_sharing(
    item_id: UUID,
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.SHARE_APPROVE)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> dict[str, str | bool]:
    try:
        result = await session.run_sync(
            lambda sync_session: approve_intelligence_sharing(
                sync_session,
                item_id=item_id,
                principal=principal,
                request_id=request_id,
            )
        )
    except GovernedDecisionError as exc:
        await session.commit()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {
        "id": str(result.item_id),
        "review_status": result.review_status,
        "share_approved": result.share_approved,
        "audit_event_id": str(result.audit_event_id),
    }


@router.post("/security/tokens/revoke", response_model=TokenRevocationResponse)
async def revoke_token(
    request: TokenRevocationRequest,
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.REVOKE_TOKENS)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> TokenRevocationResponse:
    store = TokenStateStore.from_url(settings.redis_url)
    try:
        result = await session.run_sync(
            lambda sync_session: revoke_token_with_audit(
                sync_session,
                store=store,
                principal=principal,
                jti=request.jti,
                expires_at=request.expires_at,
                reason=request.reason,
                request_id=request_id,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except TokenStateError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return TokenRevocationResponse(
        jti=result.jti,
        expires_at=result.expires_at,
        audit_event_id=str(result.audit_event_id),
    )


@router.get("/intelligence/search", response_model=SearchResponse)
async def search_intelligence(
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.READ_INTELLIGENCE)),
    ],
    q: str = Query(min_length=2, max_length=300),
    severity: str | None = Query(default=None, max_length=32),
    minimum_relevance: int = Query(default=0, ge=0, le=100),
    size: int = Query(default=50, ge=1, le=200),
) -> SearchResponse:
    del principal
    try:
        results = await search_service.search(
            q,
            severity=severity,
            minimum_relevance=minimum_relevance,
            size=size,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"search backend unavailable: {type(exc).__name__}",
        ) from exc
    return SearchResponse(query=q, count=len(results), results=results)


async def close_services() -> None:
    await database.close()
    await search_service.close()
