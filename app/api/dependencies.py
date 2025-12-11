from typing import Annotated
from uuid import UUID

from app.core.exceptions import ResourceNotFoundException
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenManager
from app.db.session import get_db_session
from app.models.user import User
from app.services.user import UserService

security = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthCredentials = Depends(security)):
    """
    Depends for take ID current user from JWT token

    args:
        credentials: HTTP Bearer credentials
    """
    token = credentials.credentials

    user_id = TokenManager.extract_user_id_from_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_current_user(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    """
    Depends for taking object current user from DB

    args:
        user_id: ID user from token
        session: DB sesssion
    """
    service = UserService(session)

    try:
        user_response = await service.get_user_by_id(user_id)
        user = await service.repository.get_by_user_id(user_id)
        return user
    except ResourceNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
