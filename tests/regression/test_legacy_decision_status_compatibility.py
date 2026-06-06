import requests

BASE_URL = "http://localhost:5000"


def _create_decision(title="Legacy needs_review decision"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": "Legacy status compatibility", "created_by": "regression-test"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_ui_home_accepts_legacy_needs_review_status():
    decision_id = _create_decision()

    approval = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/approvals",
        json={
            "approved_by": "governance-test",
            "status": "needs_review",
            "comment": "Legacy review status should not break UI routes.",
            "created_by": "regression-test",
        },
    )
    assert approval.status_code == 201

    home = requests.get(f"{BASE_URL}/ui/")
    detail = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")
    governance = requests.get(f"{BASE_URL}/ui/governance")

    assert home.status_code == 200
    assert detail.status_code == 200
    assert governance.status_code == 200
    assert "Needs Review" in home.text or "Reassessment Needed" in home.text or "Reassessment needed" in home.text
