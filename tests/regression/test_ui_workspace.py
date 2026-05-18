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
        "Context",
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


def test_ui_decision_workspace_contains_prepared_context_panels():
    session = requests.Session()
    response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={"title": "Context prepared decision", "description": "Future module hooks", "created_by": "ui-test"},
        allow_redirects=False,
    )

    assert response.status_code == 302
    detail_url = response.headers["Location"]
    detail = session.get(detail_url if detail_url.startswith("http") else f"{BASE_URL}{detail_url}")

    assert detail.status_code == 200
    assert "Process Context" in detail.text
    assert "Organization Context" in detail.text
    assert "Resource / FTE Context" in detail.text
    assert "Risk Management" in detail.text
    assert "Noch kein Prozesskontext verknüpft" in detail.text
    assert "Noch kein Organisationskontext erfasst" in detail.text
    assert "Noch keine Ressourcen- oder FTE-Grundlage" in detail.text
    assert "Noch keine Risiken bewertet" in detail.text


def test_ui_observation_reassessment_slice_is_available():
    session = requests.Session()
    response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={"title": "Observed decision", "description": "Track expected vs actual", "created_by": "ui-test"},
        allow_redirects=False,
    )

    assert response.status_code == 302
    detail_url = response.headers["Location"]
    detail_path = detail_url if detail_url.startswith("/ui/") else detail_url.replace(BASE_URL, "")
    detail = session.get(f"{BASE_URL}{detail_path}")

    assert detail.status_code == 200
    assert "Observation" in detail.text
    assert "Reassessment" in detail.text
    assert "Noch keine Beobachtung erfasst" in detail.text
    assert "Beobachtungen machen Entscheidungen überprüfbar" in detail.text

    observation = session.post(
        f"{BASE_URL}{detail_path}/observations",
        data={
            "expected_benefit": "1000",
            "actual_benefit": "800",
            "expected_cost": "500",
            "actual_cost": "700",
            "expected_risks": "Adoption risk",
            "actual_risks": "Adoption and training risk",
            "comment": "Reassessment should be considered",
            "created_by": "ui-test",
        },
        allow_redirects=True,
    )

    assert observation.status_code == 200
    assert "Schlechter als erwartet" in observation.text
    assert "Reassessment needed" in observation.text or "Reassessment Needed" in observation.text


def test_api_can_create_observation_record():
    decision_response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": "API observation decision", "description": "Observation API", "created_by": "api-test"},
    )
    assert decision_response.status_code == 201
    decision_id = decision_response.json()["id"]

    observation_response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/observations",
        json={
            "expected_benefit": 1200,
            "actual_benefit": 1300,
            "expected_cost": 600,
            "actual_cost": 600,
            "expected_risks": "Known implementation risk",
            "actual_risks": "Known implementation risk",
            "comment": "Observed after pilot",
            "created_by": "api-test",
        },
    )

    assert observation_response.status_code == 201
    body = observation_response.json()
    assert body["created_by"] == "api-test"
    assert body["status"] == "observed"


def test_ui_can_create_context_object_in_decision_workspace():
    session = requests.Session()
    response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={"title": "Context UI decision", "description": "Structured context", "created_by": "ui-test"},
        allow_redirects=False,
    )
    assert response.status_code == 302
    detail_url = response.headers["Location"]
    detail_path = detail_url if detail_url.startswith("/ui/") else detail_url.replace(BASE_URL, "")

    create_context = session.post(
        f"{BASE_URL}{detail_path}/context-objects",
        data={
            "context_type": "organization",
            "name": "Finance shared services",
            "description": "Responsible organization context",
            "source": "operating model",
            "owner": "CFO Office",
            "confidence": "high",
        },
        allow_redirects=True,
    )

    assert create_context.status_code == 200
    assert "Finance shared services" in create_context.text
    assert "Organization Context" in create_context.text
    assert "Confidence High" in create_context.text
