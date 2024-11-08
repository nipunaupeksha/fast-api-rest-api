import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from schemas.user import UserCreate, UserUpdate, UserPasswordUpdate
from models.user import User
from api.deps import get_db, get_current_user, get_current_admin_user
from sqlalchemy.orm import Session

client = TestClient(app)

# Mock data
VALID_TOKEN = "valid_token"
sample_user_data = {
    "id": uuid4(),
    "username": "testuser",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "is_admin": True,
}


# Mock functions for dependencies
def mock_get_db():
    db = MagicMock(spec=Session)
    return db


def mock_get_current_user():
    return User(**sample_user_data)


def mock_get_current_admin_user():
    admin_user_data = sample_user_data.copy()
    admin_user_data["is_admin"] = True
    return User(**admin_user_data)


@pytest.fixture(scope="module")
def authorized_client():
    app.dependency_overrides[get_db] = mock_get_db
    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[get_current_admin_user] = mock_get_current_admin_user
    yield client
    app.dependency_overrides = {}


def test_get_users_endpoint(authorized_client):
    with patch("handlers.user.get_users") as mock_get_users:
        mock_get_users.return_value = ([User(**sample_user_data)], 1)
        response = authorized_client.get("/api/v1/users/")
        assert response.status_code == 200
