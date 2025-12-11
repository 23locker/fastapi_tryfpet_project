from datetime import timedelta
from uuid import UUID

from app.core.exceptions import (
    InvalidCredentialsException,
    ResourceNotFoundException,
    UserAlreadyExistsException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import PasswordManager, TokenManager
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserResponse


class UserService:
    """Service for work with users"""

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def register_user(self, user_create: UserCreate) -> UserResponse:
        """
        Register new user

        args:
            user_create: schema for creating user
        """
        # check what new user not have email exists on finflow
        if await self.repository.user_exists(user_create.email):
            raise UserAlreadyExistsException(user_create.email)

        password_hash = PasswordManager.hash_password(user_create.password)

        # create user
        user = await self.repository.create(
            {
                "email": user_create.email,
                "first_name": user_create.first_name,
                "last_name": user_create.last_name,
                "password_hash": password_hash,
            }
        )

        await self.repository.commit()

        return UserResponse.model_validate(user)

    async def authenticate_user(
        self, user_login: UserLogin
    ) -> tuple[UserResponse, str]:
        """
        Authenticate user and return access token

        args:
            user_login: schema with email and password
        """
        user = await self.repository.get_by_email(user_login.email)

        if not user or not PasswordManager.verify_password(
            user_login.password,
            user.password_hash,
        ):
            raise InvalidCredentialsException()

        access_token = TokenManager.create_access_token(
            data={"sub": str(user._id)},
            expires_delta=timedelta(minutes=30),
        )

        return UserResponse.model_validate(user), access_token

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        """
        Take user by ID

        args:
            user_id: UUID user
        """
        user = await self.repository.get_user_by_id(user_id)

        if not user:
            raise ResourceNotFoundException("User", user_id)

        return UserResponse.model_validate(user)

    async def get_user_profile(self, user_id: UUID) -> UserResponse:
        """
        Take current user profile

        args:
            user_id: UUID user
        """
        return await self.get_user_by_id(user_id)
