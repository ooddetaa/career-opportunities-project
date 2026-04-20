# tests/test_basic.py

import pytest
import sys
import os

# Fix import path so pytest can find app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Opportunity


@pytest.fixture
def client():
    """
    Create a clean test environment with in-memory database.
    Runs before each test.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False}
    }

    with app.app_context():
        db.drop_all()      # ensure empty DB
        db.create_all()

    client = app.test_client()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_get_empty_opportunities(client):
    """
    Test GET when DB is empty
    """
    response = client.get("/api/opportunities")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_opportunity(client):
    """
    Test POST create
    """
    data = {
        "title": "Python Intern",
        "company": "Test Company",
        "location": "Peje",
        "description": "Testing API"
    }

    response = client.post("/api/opportunities", json=data)

    assert response.status_code == 201
    assert response.get_json()["title"] == "Python Intern"


def test_get_single_opportunity(client):
    """
    Test GET by id
    """
    data = {
        "title": "Backend Dev",
        "company": "Company X",
        "location": "Prishtina",
        "description": "API work"
    }

    post_response = client.post("/api/opportunities", json=data)
    created = post_response.get_json()

    response = client.get(f"/api/opportunities/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["title"] == "Backend Dev"


def test_update_opportunity(client):
    """
    Test PUT update
    """
    data = {
        "title": "Old Title",
        "company": "Company",
        "location": "City",
        "description": "Desc"
    }

    post_response = client.post("/api/opportunities", json=data)
    created = post_response.get_json()

    update_data = {
        "title": "New Title"
    }

    response = client.put(f"/api/opportunities/{created['id']}", json=update_data)

    assert response.status_code == 200
    assert response.get_json()["title"] == "New Title"


def test_delete_opportunity(client):
    """
    Test DELETE
    """
    data = {
        "title": "To Delete",
        "company": "Company",
        "location": "City",
        "description": "Desc"
    }

    post_response = client.post("/api/opportunities", json=data)
    created = post_response.get_json()

    response = client.delete(f"/api/opportunities/{created['id']}")

    assert response.status_code == 200

    # confirm deleted
    get_response = client.get(f"/api/opportunities/{created['id']}")

    assert get_response.status_code == 404