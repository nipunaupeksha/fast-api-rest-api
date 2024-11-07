from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)


# Mock function to simulate user creation
def mock_create_user(db, user):
    if user.username == "newuser":
        mock_user = MagicMock()
        mock_user.id = uuid4()
        mock_user.username = user.username
        mock_user.first_name = user.first_name
        mock_user.last_name = user.last_name
        mock_user.email = user.email
        return mock_user
    raise HTTPException(
        status_code=409, detail="A user with this username already exists."
    )


# Mock function to simulate getting the current authenticated user
def mock_get_current_user(token: str):
    if token == "valid_token":
        mock_user = MagicMock()
        mock_user.email = "testuser@example.com"
        return mock_user
    raise HTTPException(status_code=409, detail="Could not validate credentials")


# Mock function to simulate token revocation
def mock_revoke_token(db, token):
    return


# Mock function for successful authentication
def mock_authenticate_user_via_username_success(db, username, password):
    if username == "testuser" and password == "correctpassword":
        mock_user = MagicMock()
        mock_user.email = "testuser@example.com"
        return mock_user
    return None


# Mock function to simulate token validation
def mock_check_token_invalid(db, token):
    return token != "valid_token"


# Mock function for failed authentication
def mock_authenticate_user_via_username_fail(db, username, password):
    return None


# Mock function to simulate access token creation
def mock_create_access_token(db, data):
    return "sample_access_token"


def test_sign_in_success():
    with patch(
        "api.endpoints.auth.authenticate_user_via_username",
        mock_authenticate_user_via_username_success,
    ):
        with patch("api.endpoints.auth.create_access_token", mock_create_access_token):
            response = client.post(
                "/api/v1/auth/sign-in",
                data={"username": "testuser", "password": "correctpassword"},
            )
            assert response.status_code == 200
            assert "access_token" in response.json()
            assert response.json()["access_token"] == "sample_access_token"
            assert response.json()["token_type"] == "bearer"


def test_sign_in_fail():
    with patch(
        "api.endpoints.auth.authenticate_user_via_username",
        mock_authenticate_user_via_username_fail,
    ):
        response = client.post(
            "/api/v1/auth/sign-in",
            data={"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Incorrect username or password"


def test_sign_up_success():
    with patch("api.endpoints.auth.create_user", mock_create_user):
        response = client.post(
            "/api/v1/auth/sign-up",
            json={
                "username": "newuser",
                "password": "pass123",
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "is_admin": False,
            },
        )
        assert response.status_code == 201
        assert response.json()["username"] == "newuser"
        assert response.json()["email"] == "newuser@example.com"



def test_sign_out_invalid_token():
    def mock_check_token_invalid_invalid(db, token):
        return True

    with patch("api.endpoints.auth.get_current_user", mock_get_current_user):
        with patch(
            "handlers.token.check_token_invalid", mock_check_token_invalid_invalid
        ):
            headers = {"Authorization": "Bearer invalid_token"}
            response = client.post("/api/v1/auth/sign-out", headers=headers)
            assert response.status_code == 401
            assert response.json()["detail"] == "Could not validate credentials"
