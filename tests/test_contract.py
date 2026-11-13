"""Shared safety net. `python run.py check` runs this before every push."""
from __future__ import annotations

import json
import os
from pathlib import Path

import jsonschema
import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts" / "prediction.schema.json").read_text())


def validate(bundle: dict) -> None:
    jsonschema.validate(bundle, SCHEMA)


def test_fixture_matches_contract():
    validate(json.loads((ROOT / "contracts" / "fixtures" / "sample_predictions.json").read_text()))


def test_real_output_matches_contract_if_present():
    real = ROOT / "ml" / "outputs" / "predictions.json"
    if not real.exists():
        pytest.skip("no real predictions yet")
    validate(json.loads(real.read_text()))


@pytest.fixture()
def client():
    os.environ["MOCK"] = "1"
    from api.main import app
    return TestClient(app)


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_predictions_endpoint_matches_contract(client):
    r = client.get("/api/predictions")
    assert r.status_code == 200
    validate(r.json())


def test_filter_and_item(client):
    items = client.get("/api/predictions?min_score=0.5").json()["items"]
    assert all(it["score"] >= 0.5 for it in items)
    first = items[0]["id"]
    assert client.get(f"/api/items/{first}").json()["id"] == first
    assert client.get("/api/items/nope").status_code == 404


def test_app_served(client):
    assert "<html" in client.get("/").text
