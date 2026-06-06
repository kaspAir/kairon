from pathlib import Path

import requests

BASE_URL = "http://localhost:5000"


def _create_decision(title="Narrative workspace decision", description="Manual work is expensive and slow."):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": description, "created_by": "narrative-test"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_decision_detail_contains_decision_narrative_workspace():
    decision_id = _create_decision()

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Decision Brief" in response.text
    assert "Warum existiert diese Entscheidung?" in response.text
    assert "Unter welchen Umständen wird entschieden?" in response.text
    assert "Welche Optionen wurden betrachtet?" in response.text
    assert "Welche Zukunft erwarten wir?" in response.text
    assert "Was müssen wir später überprüfen?" in response.text


def test_decision_detail_narrative_is_stable_with_missing_data():
    decision_id = _create_decision("Sparse narrative decision", "")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Noch keine Entscheidungsbegründung dokumentiert." in response.text
    assert "Noch keine Optionen oder Szenarien dokumentiert." in response.text
    assert "Noch kein Reassessment definiert." in response.text


def test_relationship_awareness_keeps_summary_counts_contract():
    decision_id = _create_decision("Awareness contract decision")

    response = requests.get(f"{BASE_URL}/api/decisions/{decision_id}/relationship-awareness")

    assert response.status_code == 200
    payload = response.json()["relationship_awareness"]
    assert "summary_counts" in payload
    assert payload["summary_counts"]["processes"] == 0
    assert payload["summary_counts"]["risks"] == 0


def test_new_narrative_templates_use_translation_helper():
    template_dir = Path("app/templates/partials")
    for template_name in [
        "decision_brief.html",
        "decision_narrative_why.html",
        "decision_narrative_circumstances.html",
        "decision_narrative_options.html",
        "decision_narrative_future.html",
        "decision_narrative_reassessment.html",
    ]:
        content = (template_dir / template_name).read_text(encoding="utf-8")
        assert "t('decision_narrative." in content
