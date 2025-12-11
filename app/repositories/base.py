from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(ABC, Generic[ModelType]):
    """
    Base repository for all models, need for default CRUD operations
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, obj_in: dict) -> ModelType:
        """
        Create new post in DB

        args:
            obj_in: dict with data for create
        """

        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        """
        Take object from id

        args:
            obj_od: object id
        """

        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        """
        Take objects with pagination

        args:
            skip: how many posts for skip
            limit: max count posts
        """
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, obj_id: any, obj_in: dict) -> Optional[ModelType]:
        """
        Update existing post

        args:
            obj_id: id object
            obj_in: dict with data for update
        """
        db_obj = await self.get_by_id(obj_id)
        if not db_obj:
            return None

        for key, value in db_obj.items():
            if value is not None:
                setattr(db_obj, key, value)

        await self.session.flush()
        return db_obj

    async def delete(self, obj_id: int) -> bool:
        """
        Delete object from ID

        args:
            obj_id: ID object
        """
        db_obj = self.get_by_id(obj_id)
        if not db_obj:
            return False

        await self.session.delete(db_obj)
        await self.session.flush()
        return True

    async def commit(self):
        """commit changes for db"""
        await self.session.commit()

    async def rollback(self):
        """back changes on db"""
        await self.session.rollback()
