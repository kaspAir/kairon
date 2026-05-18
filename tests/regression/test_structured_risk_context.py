import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import requests

from app.domains.context.risk_config import ContextTaxonomy
from app.domains.context.service import DecisionContextService
from app.domains.decision.service import DecisionService
from app.shared.database import init_engine, session_scope

BASE_URL = "http://localhost:5000"


def _create_decision(title="Structured risk decision"):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": "Risk context API", "created_by": "risk-test"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_api_can_create_structured_risk_context_with_defaults():
    decision_id = _create_decision("Structured risk API defaults")

    risk_response = requests.post(
        f"{BASE_URL}/api/decisions/{decision_id}/risks",
        json={
            "name": "Supplier invoice quality risk",
            "description": "Format variability can reduce automation reliability.",
            "severity": "critical",
            "probability": "high",
            "impact": "high",
            "impact_area": "operations",
            "mitigation": "Pilot top suppliers first",
            "risk_owner": "AP Lead",
            "review_required": True,
            "confidence": "high",
        },
    )

    assert risk_response.status_code == 201
    body = risk_response.json()
    assert body["context_type"] == "risk"
    assert body["metadata_json"]["severity"] == "critical"
    assert body["metadata_json"]["review_required"] is True

    list_response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/risks")
    assert list_response.status_code == 200
    listing = list_response.json()
    assert listing["summary"]["critical"] == 1
    assert listing["taxonomy"]["severity"] == ["low", "medium", "high", "critical"]


def test_risk_context_accepts_configured_taxonomy_values_in_service_layer():
    init_engine(os.environ.get("DATABASE_URL", "sqlite:///kairon.db"))
    with session_scope() as session:
        decision = DecisionService(session).create_decision("Custom taxonomy decision", "Configured risk taxonomy")
        risk = DecisionContextService(session).create_risk_context(
            decision_id=decision.id,
            name="Cyber supply-chain exposure",
            probability="almost_certain",
            impact="severe",
            severity="extreme",
            impact_area="cyber",
            taxonomy=ContextTaxonomy(
                probability_values=("rare", "unlikely", "possible", "likely", "almost_certain"),
                impact_values=("minor", "moderate", "major", "severe"),
                severity_values=("informational", "low", "medium", "high", "extreme"),
                impact_area_values=("finance", "legal", "cyber", "customer", "supply_chain", "culture"),
            ),
        )
        assert risk.metadata_json["probability"] == "almost_certain"
        assert risk.metadata_json["impact"] == "severe"
        assert risk.metadata_json["severity"] == "extreme"
        assert risk.metadata_json["impact_area"] == "cyber"


def test_ui_renders_risk_taxonomy_values_and_created_risk_context():
    session = requests.Session()
    decision_response = session.post(
        f"{BASE_URL}/ui/decisions",
        data={"title": "UI structured risk context", "description": "Risk UI", "created_by": "risk-test"},
        allow_redirects=False,
    )
    assert decision_response.status_code == 302
    detail_path = decision_response.headers["Location"]

    detail = session.get(f"{BASE_URL}{detail_path}")
    assert detail.status_code == 200
    assert "Structured Risk Context" in detail.text
    assert "Cost" in detail.text
    assert "Compliance" in detail.text
    assert "Critical" in detail.text

    create_risk = session.post(
        f"{BASE_URL}{detail_path}/risks",
        data={
            "name": "Compliance exception risk",
            "description": "Incorrect routing could affect compliance controls.",
            "probability": "medium",
            "impact": "high",
            "severity": "critical",
            "impact_area": "compliance",
            "mitigation": "Mandatory governance review for exceptions",
            "risk_owner": "Governance Lead",
            "review_required": "on",
            "confidence": "medium",
        },
        allow_redirects=True,
    )
    assert create_risk.status_code == 200
    assert "Compliance exception risk" in create_risk.text
    assert "Critical risk" in create_risk.text
    assert "Review required" in create_risk.text


def test_dashboard_counts_critical_risk_contexts_after_demo_seed():
    requests.post(f"{BASE_URL}/ui/demo-seed", allow_redirects=False)
    dashboard = requests.get(f"{BASE_URL}/ui")

    assert dashboard.status_code == 200
    assert "Critical Risks" in dashboard.text
    assert not re.search(r'<div class="metric-value">0</div><div class="metric-label">Critical Risks', dashboard.text)
