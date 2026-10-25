from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_item():
    response = client.get("/items/2")
    assert response.status_code == 200
    assert response.json()["name"] == "test"


def test_get_missing_item_returns_404():
    response = client.get("/items/999")
    assert response.status_code == 404
