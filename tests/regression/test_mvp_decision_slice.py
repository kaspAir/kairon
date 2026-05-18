import requests

BASE_URL = "http://localhost:5000"


def test_decision_mvp_walking_skeleton():
    decision_response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": "Automate intake process", "context": "MVP governance slice", "created_by": "platform-test"},
    )
    assert decision_response.status_code == 201
    assert decision_response.json()["created_by"] == "platform-test"
    decision_id = decision_response.json()["id"]

    variant_response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/variants",
        json={"name": "Automation", "estimated_cost": 1000, "expected_benefit": 5000, "created_by": "platform-test"},
    )
    assert variant_response.status_code == 201
    assert variant_response.json()["created_by"] == "platform-test"
    variant_id = variant_response.json()["id"]

    scenario_response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/scenarios",
        json={
            "variant_id": variant_id,
            "name": "Baseline automation scenario",
            "case_volume": 120,
            "processing_minutes_per_case": 15,
            "hourly_cost": 80,
            "created_by": "platform-test",
        },
    )
    assert scenario_response.status_code == 201
    assert scenario_response.json()["created_by"] == "platform-test"
    scenario_id = scenario_response.json()["id"]

    simulation_response = requests.post(f"{BASE_URL}/api/scenarios/{scenario_id}/simulate")
    assert simulation_response.status_code == 201
    assert simulation_response.json()["total_processing_hours"] == 30.0
    assert simulation_response.json()["total_cost"] == 2400.0
    assert simulation_response.json()["impact_assessment_id"]

    risk_response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/risks",
        json={"summary": "Adoption risk", "severity": "medium", "mitigation": "Pilot first", "created_by": "platform-test"},
    )
    assert risk_response.status_code == 201
    assert risk_response.json()["created_by"] == "platform-test"

    approval_response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/approvals",
        json={"approved_by": "Architecture Board", "status": "approved", "created_by": "platform-test"},
    )
    assert approval_response.status_code == 201
    assert approval_response.json()["created_by"] == "platform-test"

    record_response = requests.post(f"{BASE_URL}/api/decisions/{decision_id}/records", json={"created_by": "platform-test"})
    assert record_response.status_code == 201
    assert record_response.json()["created_by"] == "platform-test"
    assert "AI advisory did not make this decision" in record_response.json()["record_text"]

    view_response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/record")
    assert view_response.status_code == 200
    view = view_response.json()
    assert view["title"] == "Automate intake process"
    assert view["status"] == "approved"
    assert len(view["variants"]) == 1
    assert len(view["scenarios"]) == 1
    assert view["scenarios"][0]["simulation_runs"][0]["impact_assessment"]["net_impact"] == 1600.0
    assert len(view["decision_records"]) == 1
