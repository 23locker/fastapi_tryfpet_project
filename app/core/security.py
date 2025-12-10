from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordManager:
    """Manager for work with passwords"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashing password"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Check password with hash"""
        return pwd_context.verify(plain_password, hashed_password)


class TokenManager:
    """Manager for work with JWT Tokens"""

    @staticmethod
    def create_access_token(
        data: dict[str, Any],
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create JWT Access token

        args:
            data: data for transformate to token
            expires_delta: time alive token
        """

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.security.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.security.secret_key,
            algorithm=settings.security.algorithm,
        )

        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """
        Decode JWT Token

        args:
            token: JWT Token

        raises:
            if token is not valid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm],
            )
            return payload
        except JWTError:
            raise

    @staticmethod
    def extract_user_id_from_token(token: str) -> UUID | None:
        """
        Taking user_id from token

        args:
            token: JWT token

        returns:
            UUID user or None
        """
        try:
            payload = TokenManager.decode_token(token)
            user_id = payload.get("sub")

            if user_id:
                return UUID(user_id)
            return None

        except JWTError:
            return None
