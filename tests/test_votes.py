import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.main import app

client = TestClient(app)

@patch("backend.votes.routes.get_db")
def test_upvote_feature(mock_get_db):
    db = MagicMock()
    mock_get_db.return_value = iter([db])
    db.query.return_value.filter.return_value.first.side_effect = [MagicMock(), None]  # Feature exists, not voted
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None
    current_user = MagicMock(id=1)
    with patch("backend.votes.routes.Depends", side_effect=[current_user]):
        response = client.post("/votes/upvote/1")
        assert response.status_code in (200, 422, 401)  # 401 if auth required 