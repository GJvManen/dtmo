from fastapi.testclient import TestClient

from dtmo.main import app


def test_preferences_surface_is_get_only_and_local_presentation_only() -> None:
    client = TestClient(app)
    response = client.get("/ui/preferences")
    assert response.status_code == 200
    body = response.text
    assert "RC10.6 UX polish" in body
    assert "localStorage" in body
    assert "dtmo.theme" in body
    assert "dtmo.density" in body
    assert "verlenen geen rechten" in body
    assert "share approval" in body
    assert client.post("/ui/preferences").status_code == 405


def test_preferences_values_are_allowlisted_before_application() -> None:
    response = TestClient(app).get("/ui/preferences")
    assert "['dark','light']" in response.text
    assert "['comfortable','compact']" in response.text
    assert "allowed(localStorage.getItem" in response.text
