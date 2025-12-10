from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

# create async engine for connect to DB
engine = create_async_engine(
    settings.database.async_url,
    future=True,
    echo=settings.debug,
    pool_pre_ping=True,  # check connection before use
)

# just async session
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncSession:
    """Dependency for take DB session, use in API Routes"""

    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
