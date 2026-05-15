import requests

BASE_URL = "http://localhost:5000"


def test_decision_creation_accepts_description_contract():
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": "Contract decision", "description": "Description is the API field"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "Contract decision"
    assert payload["description"] == "Description is the API field"
    assert payload["status"] == "draft"
    assert payload["version"] == 1
    assert payload["created_by"] == "system"


def test_decision_creation_rejects_missing_title():
    response = requests.post(f"{BASE_URL}/api/decisions", json={"description": "No title"})

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"]["code"] == "validation_error"


def test_not_found_response_is_structured_json():
    response = requests.get(f"{BASE_URL}/api/decisions/not-existing/record")

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "not_found"


def test_created_by_flows_through_decision_creation():
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": "Audited decision", "description": "Actor propagation", "created_by": "kaspar"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["created_by"] == "kaspar"


def test_created_by_can_be_resolved_from_header():
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        headers={"X-Kairon-User": "architecture-board"},
        json={"title": "Header actor decision", "description": "Actor from header"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["created_by"] == "architecture-board"
