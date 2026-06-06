from uuid import uuid4

import requests

from app.domains.decision.models import Decision
from app.shared.database import session_scope

BASE_URL = "http://localhost:5000"


def _create_decision(title="UI robustness decision"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": "Robustness regression", "created_by": "ui-robustness-test"},
    )
    assert response.status_code == 201
    return response.json()


def _force_decision_status(decision_id, status):
    with session_scope() as session:
        decision = session.get(Decision, decision_id)
        assert decision is not None
        decision.status = status


def test_ui_home_accepts_legacy_needs_review_status():
    decision = _create_decision("Legacy needs review decision")
    _force_decision_status(decision["id"], "needs_review")

    response = requests.get(f"{BASE_URL}/ui/")

    assert response.status_code == 200
    assert "Legacy needs review decision" in response.text
    assert "Needs Review" in response.text or "Reassessment" in response.text


def test_ui_home_accepts_unknown_legacy_status():
    decision = _create_decision("Unknown legacy status decision")
    _force_decision_status(decision["id"], "legacy_status_from_old_demo")

    response = requests.get(f"{BASE_URL}/ui/")

    assert response.status_code == 200
    assert "Unknown legacy status decision" in response.text
    assert "Needs Review" in response.text or "Reassessment" in response.text


def test_ui_missing_decision_returns_browser_friendly_response():
    missing_id = str(uuid4())

    response = requests.get(f"{BASE_URL}/ui/decisions/{missing_id}", allow_redirects=False)

    assert response.status_code in {302, 404}
    content_type = response.headers.get("content-type", "")
    assert "application/json" not in content_type


def test_demo_seed_redirect_points_to_existing_decision_and_refresh_is_stable():
    session = requests.Session()

    seed_response = session.post(f"{BASE_URL}/ui/demo-seed", allow_redirects=False)

    assert seed_response.status_code == 302
    detail_url = seed_response.headers["Location"]
    detail_path = detail_url if detail_url.startswith("/ui/") else detail_url.replace(BASE_URL, "")

    detail = session.get(f"{BASE_URL}{detail_path}")
    refresh = session.get(f"{BASE_URL}{detail_path}")
    governance = session.get(f"{BASE_URL}/ui/governance")

    assert detail.status_code == 200
    assert refresh.status_code == 200
    assert governance.status_code == 200
