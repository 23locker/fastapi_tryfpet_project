import asyncio

import uvicorn

from app.db.base import Base
from app.db.session import engine


async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  ## uncomment to clear
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully")


if __name__ == "__main__":
    asyncio.run(create_tables())

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
