from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for work with users"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Receives the user by email

        args:
            email: user email
        """
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_user_id(self, user_id: UUID) -> Optional[User]:
        """
        Take user by UUID

        args:
            user_id: UUID user
        """
        result = await self.session.execute(select(User).where(User.user_id == user_id))
        return result.scalars().first()

    async def get_activate_users(self, skip: int = 0, limit: int = 10) -> list[User]:
        """
        Get only active users

        args:
            skip: number of entries to skip
            limit: maximum number of entires
        """
        result = await self.session.execute(
            select(User).where(User.is_active == True).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def user_exists(self, email: str) -> bool:
        """
        Check what user exists with that email
        """
        result = await self.session.execute(
            select(User).where(User.email == email).limit(1)
        )
        return result.scalars().first() is not None
