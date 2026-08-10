from __future__ import annotations

import ipaddress
from datetime import UTC, datetime
from urllib.parse import urlparse

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from dtmo.persistence.models import Base


ALLOWED_SOURCE_TYPES = frozenset({"cisa-kev", "json-feed"})
ALLOWED_RELIABILITY = frozenset({"authoritative", "high", "medium", "low"})


def utc_now() -> datetime:
    return datetime.now(UTC)


def validate_source_url(value: str) -> str:
    """Validate a registry URL before it can become executable configuration.

    Only HTTPS public-host URLs are accepted. Literal non-global IP addresses,
    localhost-style names, embedded credentials and non-default ports are rejected.
    Runtime connector implementations must repeat address validation after DNS
    resolution before every outbound request to prevent DNS-rebinding SSRF.
    """
    parsed = urlparse(value.strip())
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("source URL must use https and include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("source URL must not contain embedded credentials")
    if parsed.port not in {None, 443}:
        raise ValueError("source URL must use the default HTTPS port")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith((".localhost", ".local", ".internal")):
        raise ValueError("local or internal source hostnames are not allowed")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValueError("source URL IP address must be globally routable")
    return value.strip()


class SourceDefinition(Base):
    __tablename__ = "source_definitions"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(32), index=True)
    endpoint_url: Mapped[str] = mapped_column(String(2048))
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    interval_seconds: Mapped[int] = mapped_column(Integer, default=3600)
    reliability: Mapped[str] = mapped_column(String(32), default="medium")
    secret_ref: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_by: Mapped[str] = mapped_column(String(255))
    updated_by: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    __table_args__ = (
        CheckConstraint("interval_seconds >= 60 AND interval_seconds <= 86400", name="ck_source_interval"),
        CheckConstraint("source_type IN ('cisa-kev', 'json-feed')", name="ck_source_type"),
        CheckConstraint("reliability IN ('authoritative', 'high', 'medium', 'low')", name="ck_source_reliability"),
    )


class SourceRegistry:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> list[SourceDefinition]:
        result = await self.session.scalars(select(SourceDefinition).order_by(SourceDefinition.name.asc()))
        return list(result)

    async def get(self, source_id: str) -> SourceDefinition | None:
        return await self.session.get(SourceDefinition, source_id)

    async def create(
        self,
        *,
        source_id: str,
        name: str,
        source_type: str,
        endpoint_url: str,
        enabled: bool,
        interval_seconds: int,
        reliability: str,
        secret_ref: str | None,
        actor: str,
    ) -> SourceDefinition:
        source_id = source_id.strip().lower()
        if not source_id or len(source_id) > 128 or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for ch in source_id):
            raise ValueError("source id must contain only lowercase letters, numbers, hyphen or underscore")
        if not name.strip():
            raise ValueError("source name is required")
        if source_type not in ALLOWED_SOURCE_TYPES:
            raise ValueError("unsupported source type")
        if reliability not in ALLOWED_RELIABILITY:
            raise ValueError("unsupported reliability value")
        if not 60 <= interval_seconds <= 86400:
            raise ValueError("interval_seconds must be between 60 and 86400")
        endpoint_url = validate_source_url(endpoint_url)
        if secret_ref and not secret_ref.startswith(("vault://", "secret://", "env://")):
            raise ValueError("secret_ref must be a secret reference, never a raw secret")
        if await self.get(source_id) is not None:
            raise ValueError("source id already exists")
        source = SourceDefinition(
            id=source_id,
            name=name.strip(),
            source_type=source_type,
            endpoint_url=endpoint_url,
            enabled=enabled,
            interval_seconds=interval_seconds,
            reliability=reliability,
            secret_ref=secret_ref,
            created_by=actor,
            updated_by=actor,
        )
        self.session.add(source)
        await self.session.flush()
        return source

    async def update(
        self,
        source: SourceDefinition,
        *,
        name: str | None,
        endpoint_url: str | None,
        enabled: bool | None,
        interval_seconds: int | None,
        reliability: str | None,
        secret_ref: str | None,
        actor: str,
    ) -> SourceDefinition:
        if name is not None:
            if not name.strip():
                raise ValueError("source name is required")
            source.name = name.strip()
        if endpoint_url is not None:
            source.endpoint_url = validate_source_url(endpoint_url)
        if enabled is not None:
            source.enabled = enabled
        if interval_seconds is not None:
            if not 60 <= interval_seconds <= 86400:
                raise ValueError("interval_seconds must be between 60 and 86400")
            source.interval_seconds = interval_seconds
        if reliability is not None:
            if reliability not in ALLOWED_RELIABILITY:
                raise ValueError("unsupported reliability value")
            source.reliability = reliability
        if secret_ref is not None:
            if secret_ref and not secret_ref.startswith(("vault://", "secret://", "env://")):
                raise ValueError("secret_ref must be a secret reference, never a raw secret")
            source.secret_ref = secret_ref or None
        source.updated_by = actor
        source.updated_at = utc_now()
        await self.session.flush()
        return source
