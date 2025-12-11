import pytest
from starlette.testclient import TestClient

from app.core.security import PasswordManager
from app.models.user import User


class TestHealthAPI:
    @pytest.fixture
    def sync_client(self, test_session):
        from app.db.session import get_db_session
        from app.main import app

        app.dependency_overrides[get_db_session] = lambda: test_session
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()

    def test_health_check(self, sync_client):
        response = sync_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestUserRegisterAPI:
    @pytest.fixture
    def sync_client(self, test_session):
        from app.db.session import get_db_session
        from app.main import app

        app.dependency_overrides[get_db_session] = lambda: test_session
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()

    def test_register_success(self, sync_client, test_data):
        response = sync_client.post(
            "/api/v1/users/register",
            json=test_data.VALID_USER,
        )
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["email"] == test_data.VALID_USER["email"]

    def test_register_invalid_email(self, sync_client, test_data):
        response = sync_client.post(
            "/api/v1/users/register",
            json=test_data.INVALID_EMAIL,
        )
        assert response.status_code == 422

    def test_register_short_password(self, sync_client, test_data):
        response = sync_client.post(
            "/api/v1/users/register",
            json=test_data.SHORT_PASSWORD,
        )
        assert response.status_code == 422

    def test_register_missing_fields(self, sync_client):
        response = sync_client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "first_name": "John",
            },
        )
        assert response.status_code == 422

    def test_register_duplicate_email(self, sync_client, test_session, test_data):
        user = User(
            email=test_data.VALID_USER["email"],
            first_name="Existing",
            last_name="User",
            password_hash=PasswordManager.hash_password("password123"),
        )
        test_session.add(user)
        test_session.commit()

        response = sync_client.post(
            "/api/v1/users/register",
            json=test_data.VALID_USER,
        )
        assert response.status_code == 409


class TestUserLoginAPI:
    @pytest.fixture
    def sync_client(self, test_session):
        from app.db.session import get_db_session
        from app.main import app

        app.dependency_overrides[get_db_session] = lambda: test_session
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()

    def test_login_success(self, sync_client, test_session, test_data):
        user = User(
            email=test_data.VALID_USER["email"],
            first_name=test_data.VALID_USER["first_name"],
            last_name=test_data.VALID_USER["last_name"],
            password_hash=PasswordManager.hash_password(
                test_data.VALID_USER["password"]
            ),
        )
        test_session.add(user)
        test_session.commit()

        response = sync_client.post(
            "/api/v1/users/login",
            json={
                "email": test_data.VALID_USER["email"],
                "password": test_data.VALID_USER["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_password(self, sync_client, test_session, test_data):
        user = User(
            email=test_data.VALID_USER["email"],
            first_name=test_data.VALID_USER["first_name"],
            last_name=test_data.VALID_USER["last_name"],
            password_hash=PasswordManager.hash_password(
                test_data.VALID_USER["password"]
            ),
        )
        test_session.add(user)
        test_session.commit()

        response = sync_client.post(
            "/api/v1/users/login",
            json={
                "email": test_data.VALID_USER["email"],
                "password": "WrongPassword",
            },
        )
        assert response.status_code == 401

    def test_login_user_not_found(self, sync_client, test_data):
        response = sync_client.post(
            "/api/v1/users/login",
            json={
                "email": "nonexistent@example.com",
                "password": test_data.VALID_USER["password"],
            },
        )
        assert response.status_code == 401

    def test_login_invalid_email_format(self, sync_client):
        response = sync_client.post(
            "/api/v1/users/login",
            json={
                "email": "invalid-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422


class TestUserProfileAPI:
    @pytest.fixture
    def sync_client(self, test_session):
        from app.db.session import get_db_session
        from app.main import app

        app.dependency_overrides[get_db_session] = lambda: test_session
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()

    def test_get_profile_success(self, sync_client, test_session, test_data):
        user = User(
            email=test_data.VALID_USER["email"],
            first_name=test_data.VALID_USER["first_name"],
            last_name=test_data.VALID_USER["last_name"],
            password_hash=PasswordManager.hash_password(
                test_data.VALID_USER["password"]
            ),
        )
        test_session.add(user)
        test_session.commit()

        login_response = sync_client.post(
            "/api/v1/users/login",
            json={
                "email": test_data.VALID_USER["email"],
                "password": test_data.VALID_USER["password"],
            },
        )
        token = login_response.json()["access_token"]

        response = sync_client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == test_data.VALID_USER["email"]

    def test_get_profile_no_token(self, sync_client):
        response = sync_client.get("/api/v1/users/me")
        assert response.status_code == 403

    def test_get_profile_invalid_token(self, sync_client):
        response = sync_client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401

    def test_get_profile_malformed_auth_header(self, sync_client):
        response = sync_client.get(
            "/api/v1/users/me",
            headers={"Authorization": "InvalidToken"},
        )
        assert response.status_code == 403
