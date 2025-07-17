import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.main import app
from backend.users import routes as user_routes
from backend.core import deps as core_deps

client = TestClient(app)

def test_register_user():
    db = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = None
    db.query.return_value.filter.return_value = mock_filter
    db.query.return_value.filter.side_effect = lambda *args, **kwargs: mock_filter
    # Mock user object with all required fields
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "test"
    mock_user.email = "test@example.com"
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.side_effect = lambda user: user.__setattr__('id', 1)
    db.refresh.return_value = None

    def override_get_db():
        yield db

    app.dependency_overrides[user_routes.get_db] = override_get_db

    # Simulate returning the mock user after registration
    db.refresh.side_effect = lambda user: [setattr(user, 'id', 1), setattr(user, 'username', 'test'), setattr(user, 'email', 'test@example.com')]

    response = client.post("/users/register", json={"username": "test", "email": "test@example.com", "password": "pass"})
    print(response.json())
    assert response.status_code == 200, response.json()
    assert response.json()["username"] == "test"

@patch("backend.users.routes.get_db")
def test_login_user(mock_get_db):
    db = MagicMock()
    mock_get_db.return_value = iter([db])
    # Mock user object with all required fields
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "test"
    mock_user.email = "test@example.com"
    mock_user.password_hash = "hashed"
    db.query.return_value.filter.return_value.first.return_value = mock_user
    with patch("backend.auth.auth_utils.verify_password", return_value=True):
        def override_get_db():
            yield db
        app.dependency_overrides[core_deps.get_db] = override_get_db
        response = client.post(
            "/token",
            data={"username": "test", "password": "pass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(response.json())
        assert response.status_code == 200
        assert "access_token" in response.json() 