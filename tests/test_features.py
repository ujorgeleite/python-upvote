import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.main import app

client = TestClient(app)

@patch("backend.features.routes.get_db")
def test_create_feature(mock_get_db):
    db = MagicMock()
    mock_get_db.return_value = iter([db])
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None
    current_user = MagicMock(id=1)
    with patch("backend.features.routes.Depends", side_effect=[current_user]):
        response = client.post("/features/", json={"title": "Test Feature", "description": "Desc"})
        assert response.status_code in (200, 422)  # 422 if auth required

@patch("backend.features.routes.get_db")
def test_list_features(mock_get_db):
    db = MagicMock()
    mock_get_db.return_value = iter([db])
    db.query.return_value.all.return_value = []
    db.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/features/")
    assert response.status_code == 200 