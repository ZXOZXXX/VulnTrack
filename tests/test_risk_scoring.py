
import pytest

from models.vulnerability import calculate_risk_score, get_priority


def test_risk_score_calculation():
    score = calculate_risk_score("Critical", 9, 10, 5)
    assert score == 73.5


def test_priority_categories():
    assert get_priority(85) == "Critical"
    assert get_priority(65) == "Critical"
    assert get_priority(55) == "High"
    assert get_priority(45) == "Medium"
    assert get_priority(20) == "Low"


def test_invalid_severity():
    with pytest.raises(ValueError):
        calculate_risk_score("Unknown", 5, 5, 3)


def test_invalid_exploitability():
    with pytest.raises(ValueError):
        calculate_risk_score("High", 11, 5, 3)


def test_invalid_impact():
    with pytest.raises(ValueError):
        calculate_risk_score("High", 5, 0, 3)


def test_invalid_asset_criticality():
    with pytest.raises(ValueError):
        calculate_risk_score("High", 5, 5, 6)


def test_invalid_risk_score():
    with pytest.raises(ValueError):
        get_priority(120)
