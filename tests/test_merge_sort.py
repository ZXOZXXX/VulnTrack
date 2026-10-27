
from algorithms.merge_sort import merge_sort_vulnerabilities


def test_sorts_by_risk_score_descending():
    records = [
        {"vuln_id": "VUL-001", "risk_score": 58.3},
        {"vuln_id": "VUL-002", "risk_score": 91.0},
        {"vuln_id": "VUL-003", "risk_score": 72.5},
    ]

    result = merge_sort_vulnerabilities(records)

    assert [item["risk_score"] for item in result] == [
        91.0, 72.5, 58.3
    ]


def test_empty_list():
    assert merge_sort_vulnerabilities([]) == []


def test_single_record():
    records = [{"vuln_id": "VUL-001", "risk_score": 58.3}]

    assert merge_sort_vulnerabilities(records) == records


def test_original_list_is_not_modified():
    records = [
        {"vuln_id": "VUL-001", "risk_score": 40},
        {"vuln_id": "VUL-002", "risk_score": 90},
    ]

    merge_sort_vulnerabilities(records)

    assert [item["risk_score"] for item in records] == [40, 90]


def test_sorts_by_risk_score_ascending():
    records = [
        {"vuln_id": "VUL-001", "risk_score": 58.3},
        {"vuln_id": "VUL-002", "risk_score": 91.0},
        {"vuln_id": "VUL-003", "risk_score": 72.5},
    ]

    result = merge_sort_vulnerabilities(records, descending=False)

    assert [item["risk_score"] for item in result] == [
        58.3, 72.5, 91.0
    ]


def test_descending_is_default():
    records = [
        {"vuln_id": "VUL-001", "risk_score": 40},
        {"vuln_id": "VUL-002", "risk_score": 90},
    ]

    result = merge_sort_vulnerabilities(records)

    assert [item["risk_score"] for item in result] == [90, 40]

