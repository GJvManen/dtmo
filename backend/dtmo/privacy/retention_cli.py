from __future__ import annotations

import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dtmo.config import get_settings

from .store import purge_expired_projections


def purge_all_expired(*, database_url: str, batch_size: int) -> int:
    engine = create_engine(database_url, pool_pre_ping=True)
    total = 0
    while True:
        with Session(engine) as session:
            result = purge_expired_projections(session, batch_size=batch_size)
            session.commit()
        total += result.deleted
        if result.deleted < batch_size:
            return total


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Purge expired privacy-minimized audit projections while preserving legal holds."
    )
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args()
    deleted = purge_all_expired(
        database_url=get_settings().database_url,
        batch_size=args.batch_size,
    )
    print(f"purged_audit_projections={deleted}")


if __name__ == "__main__":
    main()
