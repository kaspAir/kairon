from pathlib import Path

import requests

BASE_URL = "http://localhost:5000"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _create_decision(title="Briefing decision", description="Manual processing creates delays."):
    response = requests.post(
        f"{BASE_URL}/api/decisions",
        json={"title": title, "description": description, "created_by": "briefing-test"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_decision_briefing_header_and_summary_cards_render_in_german_by_default():
    decision_id = _create_decision()

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "Entscheidungsbriefing" in response.text
    assert "Kurzübersicht der Entscheidungsgrundlagen" in response.text
    assert "Risiken" in response.text
    assert "Szenarien" in response.text
    assert "Betroffene Prozesse" in response.text
    assert "Governance" in response.text
    assert "Beobachtungen" in response.text


def test_decision_briefing_uses_collapsed_detail_sections():
    decision_id = _create_decision("Briefing details decision")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")

    assert response.status_code == 200
    assert "<details" in response.text
    assert "Technische Pflege und Detailbereiche" in response.text
    assert "Context Object speichern" in response.text
    assert "Variante speichern" in response.text


def test_language_switch_is_available_and_english_changes_new_labels():
    decision_id = _create_decision("Language briefing decision")

    german = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}")
    english = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}", params={"lang": "en"})

    assert german.status_code == 200
    assert english.status_code == 200
    assert "Sprache" in german.text
    assert "English" in english.text
    assert "Decision Briefing" in english.text
    assert "Summary of decision evidence" in english.text


def test_missing_english_keys_fall_back_without_breaking_ui():
    decision_id = _create_decision("Fallback briefing decision")

    response = requests.get(f"{BASE_URL}/ui/decisions/{decision_id}", params={"lang": "en"})

    assert response.status_code == 200
    assert "Decision Briefing" in response.text
    assert "Noch" in response.text or "Decision Insight Summary" in response.text


def test_new_briefing_templates_use_i18n_keys():
    templates = [
        PROJECT_ROOT / "app/templates/partials/decision_briefing_header.html",
        PROJECT_ROOT / "app/templates/partials/decision_briefing_summary_cards.html",
    ]
    for template in templates:
        content = template.read_text(encoding="utf-8")
        assert "decision_briefing." in content
        assert "Decision Briefing" not in content
        assert "Risiken" not in content
        assert "Show details" not in content
