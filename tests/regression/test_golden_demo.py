from urllib.parse import urlparse

import requests

BASE_URL = "http://localhost:5000"
DEMO_TITLE = "AI-based Invoice Processing Automation"


def test_ui_can_seed_golden_demo_and_show_enterprise_decision_flow():
    session = requests.Session()
    seed_response = session.post(f"{BASE_URL}/ui/demo-seed", allow_redirects=False)

    assert seed_response.status_code == 302
    detail_url = seed_response.headers["Location"]
    parsed_detail = urlparse(detail_url)
    detail_path = parsed_detail.path if parsed_detail.path.startswith("/ui/") else detail_url.replace(BASE_URL, "").split("?", 1)[0]

    detail = session.get(f"{BASE_URL}{detail_path}")
    assert detail.status_code == 200
    assert DEMO_TITLE in detail.text
    assert "AI-assisted triage" in detail.text
    assert "AI automation with governance gate" in detail.text
    assert "Risk Management" in detail.text
    assert "Observation" in detail.text
    assert "Reassessment" in detail.text

    compare = session.get(f"{BASE_URL}{detail_path}/compare")
    assert compare.status_code == 200
    assert "Current annual invoice volume" in compare.text
    assert "30% automation with finance review" in compare.text
    assert "65% automation with exception governance" in compare.text
    assert "Impact Assessment" in compare.text
    assert "Confidence" in compare.text


def test_dashboard_uses_demo_data_instead_of_empty_state_after_seed():
    requests.post(f"{BASE_URL}/ui/demo-seed", allow_redirects=False)
    dashboard = requests.get(f"{BASE_URL}/ui")

    assert dashboard.status_code == 200
    assert DEMO_TITLE in dashboard.text
    assert "Noch keine Decision vorhanden" not in dashboard.text
    assert "Open Decisions" in dashboard.text
    assert "Recent Simulations" in dashboard.text
    assert "Reassessments Needed" in dashboard.text
