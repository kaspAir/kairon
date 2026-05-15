import requests

BASE_URL = "http://localhost:5000"


def test_mvp_ui_entrypoint_is_available():
    response = requests.get(f"{BASE_URL}/ui")

    assert response.status_code == 200
    assert "KAIRON" in response.text
    assert "Decision anlegen" in response.text


def test_mvp_ui_supports_decision_creation_flow():
    response = requests.post(
        f"{BASE_URL}/ui/decisions",
        data={"title": "UI regression decision", "description": "Created through Jinja UI", "created_by": "ui-test"},
        allow_redirects=False,
    )

    assert response.status_code == 302
    assert "/ui/decisions/" in response.headers["Location"]
