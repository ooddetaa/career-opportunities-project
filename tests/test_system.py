# tests/test_system.py

import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db


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


def test_full_user_flow(client):
    """
    SYSTEM TEST:
    Simulate full user journey.
    """
    # Step 1: create opportunity
    data = {
        "title": "System Test Job",
        "company": "SysCo",
        "location": "Peje",
        "description": "System flow"
    }

    post = client.post("/api/opportunities", json=data)
    created = post.get_json()

    # Step 2: apply to it
    apply_data = {
        "applicant_name": "Test User",
        "applicant_email": "test@test.com",
        "motivation": "I am interested"
    }

    response = client.post(f"/apply/{created['id']}", data=apply_data)

    # Step 3: check applications page loads
    app_page = client.get("/applications")

    assert response.status_code == 302  # redirect after apply
    assert app_page.status_code == 200