import requests

BASE_URL = "http://localhost:5000"


def test_ui_dashboard_control_center_is_available():
    response = requests.get(f"{BASE_URL}/ui")

    assert response.status_code == 200
    assert "Decision Control Center" in response.text
    assert "Aktuelle Decisions" in response.text
    assert "Open Decisions" in response.text
    assert "Neue Decision erfassen" in response.text
    assert "/api" in response.text


def test_ui_top_navigation_uses_real_routes_not_empty_anchors():
    response = requests.get(f"{BASE_URL}/ui")

    assert response.status_code == 200
    assert 'href="/ui/scenarios"' in response.text
    assert 'href="/ui/compare"' in response.text
    assert 'href="/ui/governance"' in response.text
    assert 'href="/ui/analytics"' in response.text
    assert 'href="/ui/system-status"' in response.text
    assert 'href="#scenarios"' not in response.text
    assert 'href="#compare"' not in response.text
    assert 'href="#governance"' not in response.text
    assert 'href="#analytics"' not in response.text


def test_ui_overview_pages_are_real_navigation_targets():
    for path, expected in [
        ("/ui/scenarios", "Scenario Overview"),
        ("/ui/compare", "Compare Overview"),
        ("/ui/governance", "Governance Overview"),
        ("/ui/analytics", "Analytics Overview"),
        ("/ui/system-status", "System Status"),
    ]:
        response = requests.get(f"{BASE_URL}{path}")
        assert response.status_code == 200
        assert expected in response.text


def test_ui_can_create_decision_and_show_workspace_sections_and_compare():
    session = requests.Session()
    response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={"title": "UI workspace decision", "description": "Visual flow", "created_by": "ui-test"},
        allow_redirects=False,
    )

    assert response.status_code == 302
    detail_url = response.headers["Location"]
    detail = session.get(detail_url if detail_url.startswith("http") else f"{BASE_URL}{detail_url}")

    assert detail.status_code == 200
    assert "Decision Workspace" in detail.text
    assert "UI workspace decision" in detail.text
    for section in [
        "Overview",
        "Variants",
        "Scenarios",
        "Simulations",
        "Compare",
        "Risks & Impact",
        "Governance",
        "Decision Record",
    ]:
        assert section in detail.text

    compare = session.get(f"{BASE_URL}{detail_url}/compare" if detail_url.startswith("/ui/") else detail_url.rstrip("/") + "/compare")
    assert compare.status_code == 200
    assert "Compare View" in compare.text


def test_ui_dashboard_exposes_decision_intelligence_metadata():
    response = requests.get(f"{BASE_URL}/ui")

    assert response.status_code == 200
    assert "Varianten" in response.text or "Noch keine Decision vorhanden" in response.text
    assert "Szenarien" in response.text or "Noch keine Decision vorhanden" in response.text
    assert "Risiken" in response.text or "Noch keine Decision vorhanden" in response.text
    assert "Letzter Simulation Status" in response.text or "Noch keine Decision vorhanden" in response.text
    assert "Confidence" in response.text or "Noch keine Decision vorhanden" in response.text
    assert "Governance State" in response.text or "Noch keine Decision vorhanden" in response.text
