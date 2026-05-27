import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import requests

from app.domains.context.process_config import get_process_taxonomy


BASE_URL = "http://localhost:5000"


def _create_decision(title="Process context decision"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={
            "title": title,
            "description": "Process context API",
            "created_by": "process-test",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_process_taxonomy_defaults_are_loaded(monkeypatch):
    monkeypatch.delenv("KAIRON_PROCESS_LEVELS", raising=False)
    monkeypatch.delenv("KAIRON_PROCESS_LEVEL_LABELS", raising=False)

    taxonomy = get_process_taxonomy()

    assert taxonomy.levels == (
        "value_stream",
        "process_domain",
        "process_group",
        "process",
        "activity",
    )
    assert taxonomy.labels == (
        "Value Stream",
        "Process Domain",
        "Process Group",
        "Process",
        "Activity",
    )


def test_api_can_create_process_context():
    decision_id = _create_decision("Process context API defaults")

    response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/process-contexts",
        json={
            "name": "Invoice-to-Pay",
            "description": "Relevant process context for automation decision.",
            "process_level": "process",
            "owner": "Finance Process Owner",
            "scope": "Finance → Core Processes → Invoice-to-Pay",
            "source": "Process workshop",
            "confidence": "high",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["context_type"] == "process"
    assert body["process_level"] == "process"
    assert body["scope"] == "Finance → Core Processes → Invoice-to-Pay"
    assert body["metadata_json"]["process_level"] == "process"

    listing = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/process-contexts")
    assert listing.status_code == 200
    list_body = listing.json()
    assert list_body["items"][0]["name"] == "Invoice-to-Pay"
    assert list_body["taxonomy"]["levels"] == [
        "value_stream",
        "process_domain",
        "process_group",
        "process",
        "activity",
    ]


def test_ui_renders_process_context_and_taxonomy():
    session = requests.Session()
    decision_response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={
            "title": "UI process context",
            "description": "Process UI",
            "created_by": "process-test",
        },
        allow_redirects=False,
    )
    assert decision_response.status_code == 302
    detail_path = decision_response.headers["Location"]

    detail = session.get(f"{BASE_URL}{detail_path}")
    assert detail.status_code == 200
    assert "Process Context" in detail.text
    assert "Prozesse sind Entscheidungsgrundlagen, kein BPMN-Modul" in detail.text
    assert "Value Stream" in detail.text
    assert "Process Domain" in detail.text
    assert "Activity" in detail.text

    create_response = session.post(
        f"{BASE_URL}{detail_path}/process-contexts",
        data={
            "name": "Invoice-to-Pay",
            "description": "Decision relevant process context.",
            "process_level": "process",
            "owner": "Finance Process Owner",
            "scope": "Finance → Core Processes → Invoice-to-Pay",
            "source": "Process workshop",
            "confidence": "high",
        },
        allow_redirects=True,
    )
    assert create_response.status_code == 200
    assert "Invoice-to-Pay" in create_response.text
    assert "Finance Process Owner" in create_response.text

    taxonomy_page = session.get(f"{BASE_URL}/ui/process-taxonomy")
    assert taxonomy_page.status_code == 200
    assert "Aktive Process Taxonomy" in taxonomy_page.text
    assert "KAIRON_PROCESS_LEVELS" in taxonomy_page.text
    assert "value_stream,process_domain,process_group,process,activity" in taxonomy_page.text
