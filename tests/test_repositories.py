from uuid import uuid4

import pytest

from app.core.security import PasswordManager
from app.models.user import User
from app.repositories.user import UserRepository


class TestUserRepository:
    """Тесты для UserRepository"""

    @pytest.fixture
    async def user_repo(self, test_session):
        """Создает репозиторий для каждого теста"""
        return UserRepository(test_session)

    @pytest.fixture
    async def test_user(self, test_session):
        """Создает тестового пользователя"""
        password = "Password123"  # Обычный пароль
        hashed = PasswordManager.hash_password(password)

        user = User(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password_hash=hashed,
        )
        test_session.add(user)
        await test_session.flush()
        return user

    async def test_create_user(self, user_repo, test_session):
        """Тест создания пользователя"""
        # Arrange
        password = "Password123"  # Обычный пароль
        hashed = PasswordManager.hash_password(password)

        user_data = {
            "email": "newuser@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "password_hash": hashed,
        }

        # Act
        user = await user_repo.create(user_data)
        await user_repo.commit()

        # Assert
        assert user.user_id is not None
        assert user.email == "newuser@example.com"
        assert user.first_name == "Jane"
        assert user.last_name == "Smith"

    async def test_get_by_email_exists(self, user_repo, test_user):
        """Тест получения пользователя по email (существует)"""
        # Act
        user = await user_repo.get_by_email("test@example.com")

        # Assert
        assert user is not None
        assert user.email == "test@example.com"
        assert user.first_name == "John"

    async def test_get_by_email_not_exists(self, user_repo):
        """Тест получения пользователя по email (не существует)"""
        # Act
        user = await user_repo.get_by_email("nonexistent@example.com")

        # Assert
        assert user is None

    async def test_get_by_user_id(self, user_repo, test_user):
        """Тест получения пользователя по UUID"""
        # Act
        user = await user_repo.get_by_user_id(test_user.user_id)

        # Assert
        assert user is not None
        assert user.user_id == test_user.user_id
        assert user.email == test_user.email

    async def test_user_exists_true(self, user_repo, test_user):
        """Тест проверки существования пользователя (существует)"""
        # Act
        exists = await user_repo.user_exists("test@example.com")

        # Assert
        assert exists is True

    async def test_user_exists_false(self, user_repo):
        """Тест проверки существования пользователя (не существует)"""
        # Act
        exists = await user_repo.user_exists("nonexistent@example.com")

        # Assert
        assert exists is False

    async def test_get_active_users(self, user_repo, test_session):
        """Тест получения активных пользователей"""
        # Arrange - создаем несколько пользователей
        password1 = "Password123"
        password2 = "Password456"

        active_user = User(
            email="active@example.com",
            first_name="Active",
            last_name="User",
            password_hash=PasswordManager.hash_password(password1),
            is_active=True,
        )

        inactive_user = User(
            email="inactive@example.com",
            first_name="Inactive",
            last_name="User",
            password_hash=PasswordManager.hash_password(password2),
            is_active=False,
        )

        test_session.add(active_user)
        test_session.add(inactive_user)
        await test_session.flush()

        # Act
        active_users = await user_repo.get_active_users()

        # Assert
        assert len(active_users) == 1
        assert active_users[0].email == "active@example.com"
        assert active_users[0].is_active is True

    async def test_update_user(self, user_repo, test_user):
        """Тест обновления пользователя"""
        # Act
        updated_user = await user_repo.update(
            test_user.user_id,
            {"first_name": "Updated", "last_name": "Name"},
        )
        await user_repo.commit()

        # Assert
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.email == "test@example.com"  # не изменился

    async def test_delete_user(self, user_repo, test_user):
        """Тест удаления пользователя"""
        # Act
        deleted = await user_repo.delete(test_user.user_id)
        await user_repo.commit()

        # Assert
        assert deleted is True

        # Проверяем что пользователь действительно удален
        user = await user_repo.get_by_user_id(test_user.user_id)
        assert user is None
