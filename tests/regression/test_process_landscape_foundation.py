import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import requests

from app.domains.context.link_config import get_context_link_types


BASE_URL = "http://localhost:5000"


def test_context_link_types_are_available():
    link_types = {link_type.key: link_type for link_type in get_context_link_types()}

    assert "process_to_decision" in link_types
    assert "process_to_risk" in link_types
    assert link_types["process_to_decision"].source_context_type == "process"
    assert link_types["process_to_decision"].target_context_type == "decision"
    assert link_types["process_to_risk"].target_context_type == "risk"


def test_process_landscape_page_renders_and_shows_created_process_context():
    session = requests.Session()

    decision_response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={
            "title": "Process landscape decision",
            "description": "Decision with process landscape context",
            "created_by": "process-landscape-test",
        },
        allow_redirects=False,
    )
    assert decision_response.status_code == 302
    detail_path = decision_response.headers["Location"]

    detail = session.get(f"{BASE_URL}{detail_path}")
    assert detail.status_code == 200
    assert "Process Landscape" in detail.text or "Prozesslandkarte" in detail.text

    create_response = session.post(
        f"{BASE_URL}{detail_path}/process-contexts",
        data={
            "name": "Invoice-to-Pay",
            "description": "Process context used for landscape regression.",
            "process_level": "process",
            "owner": "Finance Process Owner",
            "scope": "Finance -> Core Processes -> Invoice-to-Pay",
            "source": "Process workshop",
            "confidence": "high",
        },
        allow_redirects=True,
    )
    assert create_response.status_code == 200

    landscape = session.get(f"{BASE_URL}/ui/process-landscape")
    assert landscape.status_code == 200
    assert "Process Landscape" in landscape.text or "Prozesslandkarte" in landscape.text
    assert "Invoice-to-Pay" in landscape.text
    assert "Process" in landscape.text
    assert "Finance Process Owner" in landscape.text
    assert "Finance -&gt; Core Processes -&gt; Invoice-to-Pay" in landscape.text or "Finance -> Core Processes -> Invoice-to-Pay" in landscape.text
    assert "Process workshop" in landscape.text
    assert "High" in landscape.text
    assert "process_to_decision" in landscape.text
    assert "process_to_risk" in landscape.text


def test_process_landscape_api_returns_process_contexts():
    response = requests.get(f"{BASE_URL}/api/process-landscape")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "grouped" in body
    assert "context_link_config" in body
    assert any(
        link_type["key"] == "process_to_decision"
        for link_type in body["context_link_config"]["active_link_types"]
    )
