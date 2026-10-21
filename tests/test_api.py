from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app

ROOT = Path(__file__).resolve().parents[1]


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert "status" in payload


def test_predict_endpoint() -> None:
    client = TestClient(app)
    health = client.get("/health").json()
    if not health.get("model_loaded"):
        return

    response = client.post(
        "/api/predict",
        json={
            "country": "India",
            "year": 2022,
            "population": 1400000000,
            "gdp": 3400000000000,
            "cement_co2": 300,
            "coal_co2": 1800,
            "oil_co2": 650,
            "gas_co2": 150,
            "flaring_co2": 3,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "predicted_co2" in body
    assert isinstance(body["predicted_co2"], (int, float))
