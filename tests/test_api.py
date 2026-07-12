from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_score_happy_path():
    res = client.post("/api/score", json={"text": "You are granted a license to access the service at our sole discretion."})
    assert res.status_code == 200
    body = res.json()
    assert set(body) == {"dodi_score", "components", "details"}
    assert 0 <= body["dodi_score"] <= 100


def test_missing_field_is_422():
    assert client.post("/api/score", json={}).status_code == 422


def test_empty_text_is_422():
    assert client.post("/api/score", json={"text": ""}).status_code == 422


def test_whitespace_only_text_is_400():
    assert client.post("/api/score", json={"text": "   \n\t  "}).status_code == 400


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_index_serves_page():
    res = client.get("/")
    assert res.status_code == 200
    assert "DODI" in res.text
