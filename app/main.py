import re
import uuid

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.routing import APIRouter
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

# ====== create app ======
app = FastAPI(title="Tryf Pet Project")

# ======== DATABASE =========

# async engine for interaction with db
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# session for work with db
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# ====== MODELS ======

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)


# ====== all logic with db ======


class UserDAO:
    """Data layer for operation user info"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
        )
        self.db.add(new_user)
        await self.db.commit()
        return new_user


# ====== pydantic validate ======

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """need for pydantic, convert even non dict obj to json"""

        from_attributes = True


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Name should contains only letters",
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Surname should contains only letters",
            )
        return value


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


# ===== API ======

user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_dao = UserDAO(session)

            user = await user_dao.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )

            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)


# create the instance for the routes
router = APIRouter()


# set routes to the app instance
router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(router)


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
