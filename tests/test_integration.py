# tests/test_integration.py

import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Opportunity


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

    client = app.test_client()
    yield client

    with app.app_context():
        db.drop_all()


def test_create_and_read_opportunity(client):
    """
    INTEGRATION TEST:
    Test DB + route working together.
    """
    data = {
        "title": "Integration Test",
        "company": "TestCo",
        "location": "Peje",
        "description": "Integration"
    }

    # Create
    client.post("/api/opportunities", json=data)

    # Read
    response = client.get("/api/opportunities")

    assert response.status_code == 200
    assert len(response.get_json()) == 1