from pathlib import Path

import requests

BASE_URL = "http://localhost:5000"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _create_decision(title="Workspace foundation decision", description="Decision workspace rationale"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": description, "created_by": "workspace-test"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_process_context(decision_id, name="Workspace Process"):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/process-contexts",
        json={
            "name": name,
            "description": "Process context for the decision workspace.",
            "process_level": "process",
            "owner": "Process Owner",
            "scope": "Workspace scope",
            "source": "Regression test",
            "confidence": "medium",
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_risk_context(decision_id, name="Workspace Risk"):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/risks",
        json={
            "name": name,
            "description": "Risk context for the decision workspace.",
            "category": "implementation",
            "probability": "medium",
            "impact": "medium",
            "severity": "medium",
            "impact_area": "operations",
            "confidence": "medium",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_decision_detail_renders_decision_workspace_foundation():
    decision_id = _create_decision("Workspace story decision")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Decision Story Header" in response.text
    assert "Why this decision?" in response.text or "Decision Workspace" in response.text
    assert "Expected Future" in response.text
    assert "Reassessment" in response.text


def test_decision_workspace_renders_without_relationships():
    decision_id = _create_decision("Workspace empty state", "")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "No related objects have been documented yet." in response.text
    assert "No scenarios or explicit future assumptions have been documented yet." in response.text
    assert "No reassessment has been defined yet." in response.text


def test_decision_workspace_renders_related_objects_and_impact():
    decision_id = _create_decision("Workspace relationship decision")
    process = _create_process_context(decision_id, "Invoice Processing")
    risk = _create_risk_context(decision_id, "Data Quality Risk")

    create_response = requests.post(
        f"{BASE_URL}/api/context/{process['id']}/relationships",
        json={
            "type": "process_to_risk",
            "target_context_id": risk["id"],
            "target_context_type": "risk",
            "label": "Operational dependency",
            "reason": "Process delay can increase data quality risk.",
            "confidence": "medium",
        },
    )
    assert create_response.status_code == 201

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Related Objects" in response.text
    assert "Related Processes" in response.text
    assert "Related Risks" in response.text
    assert "Invoice Processing" in response.text
    assert "Data Quality Risk" in response.text
    assert "This decision is influenced by" in response.text
    assert "This decision influences" in response.text


def test_relationship_awareness_api_is_stable_for_empty_decision():
    decision_id = _create_decision("Workspace awareness API")

    response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/relationship-awareness")

    assert response.status_code == 200
    awareness = response.json()["relationship_awareness"]
    assert awareness["related_objects"]["processes"]["count"] == 0
    assert awareness["related_objects"]["risks"]["count"] == 0
    assert awareness["impact"]["influenced_by"] == []
    assert awareness["impact"]["influences"] == []


def test_new_decision_workspace_templates_use_translation_keys():
    templates = [
        PROJECT_ROOT / "app/templates/partials/decision_story_header.html",
        PROJECT_ROOT / "app/templates/partials/decision_context.html",
        PROJECT_ROOT / "app/templates/partials/expected_future.html",
        PROJECT_ROOT / "app/templates/partials/impact_map.html",
        PROJECT_ROOT / "app/templates/partials/reassessment_panel.html",
    ]
    for template in templates:
        content = template.read_text(encoding="utf-8")
        assert "decision_workspace." in content
        assert "No scenarios yet" not in content
        assert "Why this decision?" not in content
        assert "No reassessment has been defined yet." not in content
