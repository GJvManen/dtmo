from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.lake.minio_store import MinioObjectStore
from dtmo.lake.service import IntelligenceLake
from dtmo.persistence.repository import IntelligenceRepository
from dtmo.persistence.session import Database
from dtmo.search.service import OpenSearchService

from .schemas import IntelligenceIngestRequest, IntelligenceIngestResponse, SearchResponse

router = APIRouter(prefix="/api/v1", tags=["intelligence"])
database = Database()
lake = IntelligenceLake(MinioObjectStore())
search_service = OpenSearchService()


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in database.session():
        yield session


@router.post(
    "/intelligence",
    response_model=IntelligenceIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_intelligence(
    request: IntelligenceIngestRequest,
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.REVIEW_INTELLIGENCE)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
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
        "ingested_by": principal.subject,
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

    indexed = False
    if inserted:
        try:
            await search_service.index_document(
                str(item.id),
                {
                    "title": item.title,
                    "summary": item.summary,
                    "item_type": item.item_type,
                    "source_id": item.source_id,
                    "severity": item.severity,
                    "confidence": item.confidence,
                    "education_relevance": item.education_relevance,
                    "published_at": item.published_at.isoformat() if item.published_at else None,
                    "canonical_url": item.canonical_url,
                    "tags": item.tags,
                },
            )
            indexed = True
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
