import requests

BASE_URL = "http://localhost:5000"


def _create_decision(title="Context relationship decision"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={
            "title": title,
            "description": "Context relationship foundation test",
            "created_by": "relationship-test",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_process_context(decision_id, name="Relationship Process"):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/process-contexts",
        json={
            "name": name,
            "description": "Process context for relationship testing.",
            "process_level": "process",
            "owner": "Process Owner",
            "scope": "Relationship test scope",
            "source": "Regression test",
            "confidence": "medium",
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_risk_context(decision_id, name="Relationship Risk"):
    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/risks",
        json={
            "name": name,
            "description": "Risk context for relationship testing.",
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


def test_relationship_types_endpoint_returns_200():
    response = requests.get(f"{BASE_URL}/api/context/relationships/types")

    assert response.status_code == 200


def test_relationship_types_include_process_to_risk():
    response = requests.get(f"{BASE_URL}/api/context/relationships/types")
    payload = response.json()
    keys = {item["key"] for item in payload["relationship_types"]}

    assert "process_to_risk" in keys


def test_relationship_types_include_process_to_decision():
    response = requests.get(f"{BASE_URL}/api/context/relationships/types")
    payload = response.json()
    keys = {item["key"] for item in payload["relationship_types"]}

    assert "process_to_decision" in keys


def test_relationship_can_be_added_to_context_object_via_api():
    decision_id = _create_decision("API relationship attach")
    source_context = _create_process_context(decision_id, "Attach Source Process")
    target_context = _create_risk_context(decision_id, "Attach Target Risk")

    response = requests.post(
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

    assert response.status_code == 201
    body = response.json()
    assert body["relationship"]["type"] == "process_to_risk"
    assert body["relationship"]["target_context_id"] == target_context["id"]
    assert body["relationship"]["target_context_type"] == "risk"


def test_unknown_relationship_type_returns_400():
    decision_id = _create_decision("Unknown relationship type")
    source_context = _create_process_context(decision_id, "Unknown Source Process")
    target_context = _create_risk_context(decision_id, "Unknown Target Risk")

    response = requests.post(
        f"{BASE_URL}/api/context/{source_context['id']}/relationships",
        json={
            "type": "unknown_relationship",
            "target_context_id": target_context["id"],
        },
    )

    assert response.status_code == 400


def test_decision_relationship_summary_returns_relationship():
    decision_id = _create_decision("Decision relationship summary")
    source_context = _create_process_context(decision_id, "Summary Source Process")
    target_context = _create_risk_context(decision_id, "Summary Target Risk")

    create_response = requests.post(
        f"{BASE_URL}/api/context/{source_context['id']}/relationships",
        json={
            "type": "process_to_risk",
            "target_context_id": target_context["id"],
            "target_context_type": "risk",
        },
    )
    assert create_response.status_code == 201

    response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/context-relationships")
    payload = response.json()

    assert response.status_code == 200
    assert payload["summary"]
    assert payload["summary"][0]["relationships"][0]["type"] == "process_to_risk"


def test_context_relationships_ui_returns_200():
    response = requests.get(f"{BASE_URL}/ui/context-relationships")

    assert response.status_code == 200


def test_context_relationships_ui_shows_relationship_type_labels():
    response = requests.get(f"{BASE_URL}/ui/context-relationships")

    assert response.status_code == 200
    assert "Process to Risk" in response.text
    assert "Process to Decision" in response.text


def test_process_landscape_shows_relationship_count_or_link():
    response = requests.get(f"{BASE_URL}/ui/process-landscape")

    assert response.status_code == 200
    assert "Relationships" in response.text or "context-relationships" in response.text
