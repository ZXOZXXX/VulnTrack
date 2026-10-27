
from algorithms.linear_search import linear_search_vulnerability


def test_finds_existing_vulnerability():
    records = [
        {"vuln_id": "VUL-001", "title": "SQL Injection"},
        {"vuln_id": "VUL-002", "title": "Cross-Site Scripting"},
    ]

    result = linear_search_vulnerability(records, "VUL-002")

    assert result == records[1]


def test_returns_none_when_not_found():
    records = [
        {"vuln_id": "VUL-001", "title": "SQL Injection"},
    ]

    assert linear_search_vulnerability(records, "VUL-999") is None


def test_search_is_case_insensitive():
    records = [
        {"vuln_id": "VUL-001", "title": "SQL Injection"},
    ]

    assert linear_search_vulnerability(records, "vul-001") == records[0]


def test_search_ignores_surrounding_spaces():
    records = [
        {"vuln_id": "VUL-001", "title": "SQL Injection"},
    ]

    assert linear_search_vulnerability(records, " VUL-001 ") == records[0]


def test_empty_list():
    assert linear_search_vulnerability([], "VUL-001") is None
