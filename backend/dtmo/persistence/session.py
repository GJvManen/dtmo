from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from dtmo.config import Settings, get_settings


class Database:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.engine: AsyncEngine = create_async_engine(
            self.settings.database_url,
            pool_pre_ping=True,
            pool_recycle=1800,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def ping(self) -> bool:
        try:
            async with self.engine.connect() as connection:
                await connection.exec_driver_sql("SELECT 1")
            return True
        except Exception:
            return False

    async def close(self) -> None:
        await self.engine.dispose()
