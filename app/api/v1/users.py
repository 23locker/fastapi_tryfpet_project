from typing import Annotated

from app.core.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_create: UserCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Register new user

    - email: user email
    - first_name: name
    - last_name: surname
    - password: password (minimum 8 characters)
    """
    service = UserService(session)

    try:
        user = await service.register_user(user_create)
        return user
    except UserAlreadyExistsException as e:
        raise e.to_http_exception()


class TokenResponse(UserResponse):
    """Response with token after login"""

    access_token: str
    token_type: str = "bearer"


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    user_login: UserLogin,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Login user and return access token

    - email: email user
    - password: password
    """
    service = UserService(session)

    try:
        user_responce, access_token = await service.authenticate_user(user_login)
        return {
            **user_responce.model_dump(),
            "access_token": access_token,
        }
    except InvalidCredentialsException as e:
        raise e.to_http_exception()


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Take profile current user
    requires authentication (Bearer token).
    """
    return UserResponse.model_validate(current_user)
