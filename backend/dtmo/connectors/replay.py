from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, Session, mapped_column

from dtmo.persistence.models import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class ConnectorReplayClaim(Base):
    __tablename__ = "connector_replay_claims"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    connector_id: Mapped[str] = mapped_column(String(128), index=True)
    external_id: Mapped[str] = mapped_column(String(255), index=True)
    payload_digest: Mapped[str] = mapped_column(String(64))
    first_run_id: Mapped[UUID] = mapped_column(index=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    source_uri: Mapped[str] = mapped_column(String(2048))
    publish_approved: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(
            "connector_id", "external_id", "payload_digest", name="uq_connector_replay_claim"
        ),
    )


class ConnectorReplayStore:
    """Persistent idempotency registry for accepted connector candidates.

    A claim is unique by connector, upstream external ID and canonical payload digest.
    Replaying the same upstream intelligence in a later run therefore fails closed,
    while a materially changed upstream payload can be processed as a new candidate.
    Claims never grant publication approval.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def is_replay(self, *, connector_id: str, external_id: str, payload_digest: str) -> bool:
        statement = select(ConnectorReplayClaim.id).where(
            ConnectorReplayClaim.connector_id == connector_id,
            ConnectorReplayClaim.external_id == external_id,
            ConnectorReplayClaim.payload_digest == payload_digest,
        )
        return self.session.scalar(statement) is not None

    def claim(
        self,
        *,
        connector_id: str,
        external_id: str,
        payload_digest: str,
        run_id: UUID,
        source_uri: str,
        observed_at: datetime | None = None,
    ) -> bool:
        if self.is_replay(
            connector_id=connector_id,
            external_id=external_id,
            payload_digest=payload_digest,
        ):
            return False
        self.session.add(
            ConnectorReplayClaim(
                connector_id=connector_id,
                external_id=external_id,
                payload_digest=payload_digest,
                first_run_id=run_id,
                first_seen_at=observed_at or utc_now(),
                source_uri=source_uri,
                publish_approved=False,
            )
        )
        try:
            self.session.flush()
        except IntegrityError:
            self.session.rollback()
            return False
        return True
