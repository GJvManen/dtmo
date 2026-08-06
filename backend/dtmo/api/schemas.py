from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import AnyHttpUrl, BaseModel, Field


class ProvenanceInput(BaseModel):
    source_url: AnyHttpUrl
    source_title: str | None = None
    publisher: str | None = None
    exact_passage: str | None = None
    confidence: int = Field(default=50, ge=0, le=100)


class IntelligenceIngestRequest(BaseModel):
    source_id: str = Field(min_length=2, max_length=128)
    external_id: str | None = Field(default=None, max_length=255)
    item_type: str = Field(default="article", max_length=64)
    title: str = Field(min_length=3, max_length=500)
    summary: str = ""
    canonical_url: AnyHttpUrl
    published_at: datetime | None = None
    severity: str = Field(default="informational", max_length=32)
    confidence: int = Field(default=50, ge=0, le=100)
    education_relevance: int = Field(default=0, ge=0, le=100)
    tags: list[str] = Field(default_factory=list, max_length=100)
    metadata: dict[str, Any] = Field(default_factory=dict)
    provenance: list[ProvenanceInput] = Field(min_length=1)
    raw_payload: dict[str, Any]


class IntelligenceIngestResponse(BaseModel):
    id: str
    inserted: bool
    review_status: str
    share_approved: bool
    raw_object_key: str
    raw_sha256: str
    indexed: bool


class TokenRevocationRequest(BaseModel):
    jti: str = Field(min_length=1, max_length=255)
    expires_at: datetime
    reason: str = Field(min_length=3, max_length=500)


class TokenRevocationResponse(BaseModel):
    jti: str
    expires_at: datetime
    audit_event_id: str
    revoked: bool = True


class SearchResponse(BaseModel):
    query: str
    count: int
    results: list[dict[str, Any]]
