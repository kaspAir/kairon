import requests

BASE_URL = "http://localhost:5000"


def _create_decision(title="Relationship awareness decision"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={
            "title": title,
            "description": "Relationship awareness foundation test",
            "created_by": "relationship-awareness-test",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_process_context(decision_id, name="Awareness Process"):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/process-contexts",
        json={
            "name": name,
            "description": "Process context for relationship awareness testing.",
            "process_level": "process",
            "owner": "Process Owner",
            "scope": "Relationship awareness test scope",
            "source": "Regression test",
            "confidence": "medium",
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_risk_context(decision_id, name="Awareness Risk"):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/risks",
        json={
            "name": name,
            "description": "Risk context for relationship awareness testing.",
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


def test_decision_detail_returns_200_without_relationships():
    decision_id = _create_decision("Awareness empty detail")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200


def test_decision_detail_shows_related_objects_section():
    decision_id = _create_decision("Awareness UI section")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Related Objects" in response.text


def test_relationship_awareness_api_returns_empty_stable_structure():
    decision_id = _create_decision("Awareness empty API")

    response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/relationship-awareness")
    payload = response.json()

    assert response.status_code == 200
    awareness = payload["relationship_awareness"]
    assert "related_objects" in awareness
    assert "impact" in awareness
    assert awareness["related_objects"]["processes"]["count"] == 0
    assert awareness["related_objects"]["risks"]["count"] == 0
    assert awareness["impact"]["influenced_by"] == []
    assert awareness["impact"]["influences"] == []


def test_process_to_risk_relationship_appears_in_related_objects():
    decision_id = _create_decision("Awareness process to risk")
    source_context = _create_process_context(decision_id, "Invoice Processing")
    target_context = _create_risk_context(decision_id, "Compliance Risk")

    create_response = requests.post(
        f"{BASE_URL}/api/context/{source_context['id']}/relationships",
        json={
            "type": "process_to_risk",
            "target_context_id": target_context["id"],
            "target_context_type": "risk",
            "label": "Operational dependency",
            "reason": "Activity delay increases operational risk",
            "confidence": "medium",
        },
    )
    assert create_response.status_code == 201

    response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/relationship-awareness")
    awareness = response.json()["relationship_awareness"]

    assert response.status_code == 200
    risk_names = {item["name"] for item in awareness["related_objects"]["risks"]["items"]}
    assert "Compliance Risk" in risk_names


def test_decision_to_context_relationship_counts_are_correct():
    decision_id = _create_decision("Awareness summary counts")
    source_context = _create_process_context(decision_id, "Procurement Process")
    target_context = _create_risk_context(decision_id, "Data Quality Risk")

    create_response = requests.post(
        f"{BASE_URL}/api/context/{source_context['id']}/relationships",
        json={
            "type": "decision_to_context",
            "target_context_id": target_context["id"],
            "target_context_type": "risk",
            "label": "Relevant context",
        },
    )
    assert create_response.status_code == 201

    response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/relationship-awareness")
    awareness = response.json()["relationship_awareness"]

    assert response.status_code == 200
    assert awareness["related_objects"]["processes"]["count"] == 1
    assert awareness["related_objects"]["risks"]["count"] == 1
    assert awareness["summary_counts"]["processes"] == 1
    assert awareness["summary_counts"]["risks"] == 1


def test_decision_detail_shows_related_relationship_object_name():
    decision_id = _create_decision("Awareness UI object")
    source_context = _create_process_context(decision_id, "AP Process")
    target_context = _create_risk_context(decision_id, "Change Resistance")

    create_response = requests.post(
        f"{BASE_URL}/api/context/{source_context['id']}/relationships",
        json={
            "type": "process_to_risk",
            "target_context_id": target_context["id"],
            "target_context_type": "risk",
        },
    )
    assert create_response.status_code == 201

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Change Resistance" in response.text
