# tests/test_unit.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import opportunity_to_dict
from models import Opportunity


def test_opportunity_to_dict():
    """
    UNIT TEST:
    Test a small function (no database, no routes).
    """
    opp = Opportunity(
        id=1,
        title="Test",
        company="Company",
        location="City",
        description="Desc"
    )

    result = opportunity_to_dict(opp)

    assert result["title"] == "Test"
    assert result["company"] == "Company"