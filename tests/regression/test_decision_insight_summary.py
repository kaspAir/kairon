from pathlib import Path

import requests

BASE_URL = "http://localhost:5000"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _create_decision(title="Insight decision", description="Manual effort should be reduced."):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": description, "created_by": "insight-test"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_variant(decision_id, name, estimated_cost, expected_benefit):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/variants",
        json={
            "name": name,
            "description": f"{name} description",
            "estimated_cost": estimated_cost,
            "expected_benefit": expected_benefit,
            "created_by": "insight-test",
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_scenario(decision_id, variant_id, name="Insight scenario"):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/scenarios",
        json={
            "variant_id": variant_id,
            "name": name,
            "description": "Scenario for insight summary",
            "case_volume": 48000,
            "processing_minutes_per_case": 15,
            "hourly_cost": 80,
            "created_by": "insight-test",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_decision_detail_renders_insight_summary_for_sparse_decision():
    decision_id = _create_decision("Sparse insight decision", "")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Decision Insight Summary" in response.text
    assert "Noch nicht genügend Informationen" in response.text
    assert "Decision Levers" in response.text


def test_decision_detail_renders_key_findings_for_options_and_scenarios():
    decision_id = _create_decision("Compared insight decision")
    variant_a = _create_variant(decision_id, "Variant A", 10000, 15000)
    variant_b = _create_variant(decision_id, "Variant B", 10000, 30000)
    scenario = _create_scenario(decision_id, variant_b["id"])

    simulation_response = requests.post(f"{BASE_URL}/api/scenarios/{scenario['id']}/simulate", json={"created_by": "insight-test"})
    assert simulation_response.status_code == 201

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Zentrale Hinweise" in response.text
    assert "Variant B" in response.text
    assert "Simulationsergebnis" in response.text
    assert "Nächster sinnvoller Schritt" in response.text


def test_decision_lever_adjustment_renders_consequence_preview():
    decision_id = _create_decision("Lever insight decision")
    variant = _create_variant(decision_id, "Variant Lever", 5000, 20000)
    _create_scenario(decision_id, variant["id"])

    response = requests.get(
        f"{BASE_URL}/ui/decisions/{decision_id}",
        params={
            "insight_case_volume": "48000",
            "insight_processing_minutes_per_case": "25",
            "insight_hourly_cost": "80",
            "insight_expected_benefit": "40000",
            "insight_estimated_cost": "5000",
            "insight_time_horizon_years": "3",
            "insight_risk_severity": "high",
            "insight_confidence": "medium",
        },
    )

    assert response.status_code == 200
    assert "Konsequenzvorschau" in response.text
    assert "3 Jahr" in response.text
    assert "zusätzliche Risikoprüfung" in response.text


def test_decision_insight_template_uses_i18n_keys():
    template = PROJECT_ROOT / "app/templates/partials/decision_insight_summary.html"
    content = template.read_text(encoding="utf-8")

    assert "decision_insight." in content
    assert "Decision Insight Summary" not in content
    assert "Not enough information" not in content
    assert "Choose Variant" not in content
