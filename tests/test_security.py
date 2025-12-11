"""
Тесты для модуля security (пароли, токены)
"""

import pytest

from app.core.security import PasswordManager, TokenManager


class TestPasswordManager:
    """Тесты для управления паролями"""

    def test_hash_password(self):
        """Тест хеширования пароля"""
        password = "testpass123"
        hashed = PasswordManager.hash_password(password)

        assert hashed != password
        assert PasswordManager.verify_password(password, hashed)

    def test_verify_password_invalid(self):
        """Тест проверки неверного пароля"""
        password = "testpass123"
        hashed = PasswordManager.hash_password(password)

        assert not PasswordManager.verify_password("wrongpass", hashed)

    def test_hash_different_each_time(self):
        """Тест что хеши разные для одного пароля"""
        password = "testpass123"
        hash1 = PasswordManager.hash_password(password)
        hash2 = PasswordManager.hash_password(password)

        assert hash1 != hash2
        assert PasswordManager.verify_password(password, hash1)
        assert PasswordManager.verify_password(password, hash2)

    def test_hash_empty_password(self):
        """Тест хеширования пустого пароля"""
        password = ""
        hashed = PasswordManager.hash_password(password)

        assert PasswordManager.verify_password(password, hashed)

    def test_verify_password_case_sensitive(self):
        """Тест что проверка пароля чувствительна к регистру"""
        password = "TestPass123"
        hashed = PasswordManager.hash_password(password)

        assert not PasswordManager.verify_password("testpass123", hashed)


class TestTokenManager:
    """Тесты для управления JWT токенами"""

    def test_create_access_token(self):
        """Тест создания JWT токена"""
        data = {"sub": "123e4567-e89b-12d3-a456-426614174000"}
        token = TokenManager.create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_token(self):
        """Тест декодирования токена"""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        data = {"sub": user_id}
        token = TokenManager.create_access_token(data)

        decoded = TokenManager.decode_token(token)
        assert decoded["sub"] == user_id

    def test_extract_user_id_from_token(self):
        """Тест извлечения user_id из токена"""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        data = {"sub": user_id}
        token = TokenManager.create_access_token(data)

        extracted_id = TokenManager.extract_user_id_from_token(token)
        assert str(extracted_id) == user_id

    def test_extract_user_id_invalid_token(self):
        """Тест извлечения user_id из невалидного токена"""
        result = TokenManager.extract_user_id_from_token("invalid_token")
        assert result is None

    def test_extract_user_id_none_sub(self):
        """Тест извлечения при отсутствии sub в токене"""
        data = {"some_other_field": "value"}
        token = TokenManager.create_access_token(data)

        result = TokenManager.extract_user_id_from_token(token)
        assert result is None

    def test_token_contains_exp(self):
        """Тест что токен содержит время истечения"""
        data = {"sub": "user123"}
        token = TokenManager.create_access_token(data)

        decoded = TokenManager.decode_token(token)
        assert "exp" in decoded
