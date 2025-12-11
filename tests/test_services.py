import pytest

from app.core.exceptions import (
    InvalidCredentialsException,
    ResourceNotFoundException,
    UserAlreadyExistsException,
)
from app.core.security import PasswordManager
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user import UserService


class TestUserService:
    @pytest.fixture
    async def user_service(self, test_session):
        return UserService(test_session)

    @pytest.fixture
    async def existing_user(self, test_session):
        password = "Password123"
        hashed = PasswordManager.hash_password(password)

        user = User(
            email="existing@example.com",
            first_name="Existing",
            last_name="User",
            password_hash=hashed,
            is_active=True,
        )
        test_session.add(user)
        await test_session.commit()
        return user

    async def test_register_user_success(self, user_service, test_session):
        user_create = UserCreate(
            email="newuser@example.com",
            first_name="John",
            last_name="Doe",
            password="SecurePassword123",
        )

        user_response = await user_service.register_user(user_create)
        await test_session.commit()

        assert user_response.user_id is not None
        assert user_response.email == "newuser@example.com"
        assert user_response.first_name == "John"
        assert user_response.last_name == "Doe"
        assert user_response.is_active is True
        assert user_response.is_verified is False

    async def test_register_user_duplicate_email(self, user_service, existing_user):
        user_create = UserCreate(
            email="existing@example.com",
            first_name="Another",
            last_name="User",
            password="Password123",
        )

        with pytest.raises(UserAlreadyExistsException):
            await user_service.register_user(user_create)

    async def test_register_password_hashed(self, user_service, test_session):
        user_create = UserCreate(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="PlainPassword123",
        )

        user_response = await user_service.register_user(user_create)
        await test_session.commit()

        user_in_db = await user_service.repository.get_by_email("test@example.com")
        assert user_in_db.password_hash != "PlainPassword123"
        assert PasswordManager.verify_password(
            "PlainPassword123", user_in_db.password_hash
        )

    async def test_authenticate_user_success(self, user_service, existing_user):
        user_login = UserLogin(
            email="existing@example.com",
            password="Password123",
        )

        user_response, access_token = await user_service.authenticate_user(user_login)

        assert user_response.user_id == existing_user.user_id
        assert user_response.email == "existing@example.com"
        assert access_token is not None
        assert isinstance(access_token, str)
        assert len(access_token) > 0

    async def test_authenticate_wrong_password(self, user_service, existing_user):
        user_login = UserLogin(
            email="existing@example.com",
            password="WrongPassword123",
        )

        with pytest.raises(InvalidCredentialsException):
            await user_service.authenticate_user(user_login)

    async def test_authenticate_nonexistent_user(self, user_service):
        user_login = UserLogin(
            email="nonexistent@example.com",
            password="Password123",
        )

        with pytest.raises(InvalidCredentialsException):
            await user_service.authenticate_user(user_login)

    async def test_authenticate_returns_valid_token(self, user_service, existing_user):
        from app.core.security import TokenManager

        user_login = UserLogin(
            email="existing@example.com",
            password="Password123",
        )

        _, access_token = await user_service.authenticate_user(user_login)
        payload = TokenManager.decode_token(access_token)

        assert payload["sub"] == str(existing_user.user_id)

    async def test_get_user_by_id(self, user_service, existing_user):
        user_response = await user_service.get_user_by_id(existing_user.user_id)

        assert user_response.user_id == existing_user.user_id
        assert user_response.email == "existing@example.com"
        assert user_response.first_name == "Existing"

    async def test_get_user_by_id_not_found(self, user_service):
        from uuid import uuid4

        fake_id = uuid4()

        with pytest.raises(ResourceNotFoundException):
            await user_service.get_user_by_id(fake_id)

    async def test_get_user_profile(self, user_service, existing_user):
        user_response = await user_service.get_user_profile(existing_user.user_id)

        assert user_response.user_id == existing_user.user_id
        assert user_response.email == "existing@example.com"

    async def test_user_response_contains_all_fields(self, user_service, existing_user):
        user_response = await user_service.get_user_by_id(existing_user.user_id)

        assert hasattr(user_response, "user_id")
        assert hasattr(user_response, "email")
        assert hasattr(user_response, "first_name")
        assert hasattr(user_response, "last_name")
        assert hasattr(user_response, "is_active")
        assert hasattr(user_response, "is_verified")
        assert hasattr(user_response, "created_at")
        assert hasattr(user_response, "updated_at")
