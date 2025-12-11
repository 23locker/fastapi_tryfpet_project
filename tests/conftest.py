"""
conftest.py — Общие fixtures для всех тестов
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app


@pytest.fixture
async def test_db_session():
    """Создание временной тестовой БД (SQLite in-memory)"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def client(test_db_session):
    """TestClient для тестирования API"""

    async def override_get_db_session():
        yield test_db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def valid_user_data():
    """Валидные данные для создания пользователя"""
    return {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepass123",
    }


@pytest.fixture
def invalid_user_data():
    """Невалидные данные (короткий пароль)"""
    return {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "short",
    }
