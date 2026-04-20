# tests/test_mock_patch.py

import pytest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

    client = app.test_client()
    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_apply_opportunity_with_mocked_notification(client):
    """
    MOCK/PATCH TEST:
    - create an opportunity
    - apply to it
    - patch the notification function so no real external action happens
    - verify the function was called
    """
    # First create an opportunity through the API
    opportunity_data = {
        "title": "QA Intern",
        "company": "Test Company",
        "location": "Peje",
        "description": "Testing position"
    }

    create_response = client.post("/api/opportunities", json=opportunity_data)
    created_opportunity = create_response.get_json()

    # Patch the function where it is USED: inside app.py
    with patch("app.send_application_notification") as mock_notification:
        apply_data = {
            "applicant_name": "Odeta Test",
            "applicant_email": "odeta@test.com",
            "motivation": "I want to apply for this position."
        }

        response = client.post(
            f"/apply/{created_opportunity['id']}",
            data=apply_data
        )

        # Route should redirect after successful form submission
        assert response.status_code == 302

        # Check that the mocked notification function was called once
        mock_notification.assert_called_once_with(
            "Odeta Test",
            "odeta@test.com",
            "QA Intern"
        )