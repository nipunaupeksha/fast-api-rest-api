import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, Depends
from unittest.mock import patch, MagicMock
from main import app
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate, UserPasswordUpdate
from api.deps import oauth2_scheme
from models.user import User

client = TestClient(app)

# Define a valid token for authorization in tests
VALID_TOKEN = "valid_token"

# Sample data for testing
sample_user_data = {
    "id": uuid4(),
    "username": "testuser",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "is_admin": True,
}


# Mock functions
def mock_get_users(
    db: Session, limit, offset, first_name, last_name, is_admin, email, username
):
    mock_user = MagicMock()
    mock_user.__dict__.update(sample_user_data)
    return [mock_user], 1


def mock_create_user(db: Session, user: UserCreate):
    mock_user = MagicMock()
    mock_user.__dict__.update(sample_user_data)
    return mock_user


def mock_delete_user(db: Session, user: User):
    mock_user = MagicMock()
    mock_user.__dict__.update(sample_user_data)
    return mock_user


def mock_update_user(db: Session, user_id, user_update: UserUpdate):
    mock_user = MagicMock()
    mock_user.__dict__.update(sample_user_data)
    return mock_user


def mock_get_user_by_id(db: Session, user_id):
    if str(user_id) == str(sample_user_data["id"]):
        mock_user = MagicMock()
        mock_user.__dict__.update(sample_user_data)
        return mock_user
    return None


def mock_get_current_user(token: str = Depends(oauth2_scheme)):
    if token == VALID_TOKEN:
        mock_user = MagicMock()
        mock_user.__dict__.update(sample_user_data)
        return mock_user
    raise HTTPException(status_code=401, detail="Could not validate credentials")


def mock_get_current_admin_user(token: str = Depends(oauth2_scheme)):
    if token == VALID_TOKEN:
        admin_user = MagicMock()
        admin_user.__dict__.update({**sample_user_data, "is_admin": True})
        return admin_user
    raise HTTPException(status_code=403, detail="Admin privileges required")


# Override dependencies globally for the client
@pytest.fixture(scope="module")
def authorized_client():
    app.dependency_overrides[oauth2_scheme] = lambda: VALID_TOKEN
    app.dependency_overrides[mock_get_current_user] = mock_get_current_user
    app.dependency_overrides[mock_get_current_admin_user] = mock_get_current_admin_user
    yield client
    app.dependency_overrides = {}


# Test cases using the authorized_client fixture
def test_get_users(authorized_client):
    with patch("handlers.user.get_users", mock_get_users):
        headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
        response = authorized_client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 200
        assert response.json()["totalResults"] == 1


def test_create_user(authorized_client):
    with patch("handlers.user.create_user", mock_create_user):
        headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "pass123",
            "is_admin": False,
        }
        response = authorized_client.post(
            "/api/v1/users/", json=new_user_data, headers=headers
        )
        assert response.status_code == 201
        assert response.json()["username"] == "newuser"


def test_delete_user(authorized_client):
    with patch("handlers.user.get_user_by_id", mock_get_user_by_id):
        with patch("handlers.user.delete_user", mock_delete_user):
            headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
            user_id = str(sample_user_data["id"])
            response = authorized_client.delete(
                f"/api/v1/users/{user_id}", headers=headers
            )
            assert response.status_code == 200
            assert response.json()["username"] == sample_user_data["username"]


def test_update_user(authorized_client):
    with patch("handlers.user.get_user_by_id", mock_get_user_by_id):
        with patch("handlers.user.update_user", mock_update_user):
            headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
            user_id = str(sample_user_data["id"])
            update_data = {
                "first_name": "first",
                "last_name": "last",
            }
            response = authorized_client.patch(
                f"/api/v1/users/{user_id}", json=update_data, headers=headers
            )
            assert response.status_code == 200
            assert response.json()["first_name"] == "first"


def test_get_user_by_id(authorized_client):
    with patch("handlers.user.get_user_by_id", mock_get_user_by_id):
        headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
        user_id = str(sample_user_data["id"])
        response = authorized_client.get(f"/api/v1/users/{user_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == sample_user_data["username"]


def test_update_user_password(authorized_client):
    def mock_update_user_password(
        db: Session, user_id: UUID, password_data: UserPasswordUpdate
    ):
        if user_id == sample_user_data["id"]:
            return MagicMock()
        return None

    with patch("handlers.user.get_user_by_id", mock_get_user_by_id):
        with patch("handlers.user.update_user_password", mock_update_user_password):
            headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
            user_id = str(sample_user_data["id"])
            password_data = {
                "old_password": "123456789",
                "new_password": "1234567890",
            }
            response = authorized_client.patch(
                f"/api/v1/users/password/{user_id}", json=password_data, headers=headers
            )
            assert response.status_code == 200
