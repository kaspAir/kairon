import requests

BASE_URL = "http://localhost:5000"


def _create_decision(title="Lifecycle decision"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": "Controlled status transitions", "created_by": "lifecycle-test"},
    )
    assert response.status_code == 201
    return response.json()


def test_api_allows_valid_decision_status_transition():
    decision = _create_decision("Valid lifecycle transition")

    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision['id']}/status",
        json={"status": "in_review", "created_by": "lifecycle-test"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["previous_status"] == "draft"
    assert payload["status"] == "in_review"
    assert "simulated" in payload["allowed_next_statuses"]
    assert payload["version"] == 2
    assert "Decision Record integration prepared" in payload["audit_notice"]


def test_api_rejects_invalid_decision_status_transition():
    decision = _create_decision("Invalid lifecycle transition")

    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision['id']}/status",
        json={"status": "approved", "created_by": "lifecycle-test"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"]["code"] == "bad_request"
    assert "Invalid decision status transition" in payload["error"]["message"]


def test_ui_decision_workspace_exposes_lifecycle_actions():
    session = requests.Session()
    response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={"title": "UI lifecycle decision", "description": "Lifecycle actions", "created_by": "ui-test"},
        allow_redirects=False,
    )
    assert response.status_code == 302
    detail_url = response.headers["Location"]
    detail_path = detail_url if detail_url.startswith("/ui/") else detail_url.replace(BASE_URL, "")

    detail = session.get(f"{BASE_URL}{detail_path}")
    assert detail.status_code == 200
    assert "Decision Lifecycle" in detail.text
    assert "Status kontrolliert führen" in detail.text
    assert "Set In Review" in detail.text
    assert "Set Approved" not in detail.text

    transition = session.post(
        f"{BASE_URL}{detail_path}/status",
        data={"status": "in_review", "created_by": "ui-test"},
        allow_redirects=True,
    )
    assert transition.status_code == 200
    assert "Status changed to In Review" in transition.text
