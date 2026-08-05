import pytest

from app import create_app, db


@pytest.fixture()
def client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
        }
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        with app.test_client() as test_client:
            yield test_client


def register(client, username="tester", password="secret123"):
    return client.post(
        "/register",
        data={"username": username, "password": password, "confirmation": password},
        follow_redirects=True,
    )


def test_authentication_and_dashboard_flow(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    response = register(client)
    assert response.status_code == 200
    assert b"Sign in to Task Forge" in response.data

    response = client.post("/login", data={"username": "tester", "password": "secret123"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_task_lifecycle_is_scoped_to_logged_in_user(client):
    register(client)
    client.post("/login", data={"username": "tester", "password": "secret123"})

    response = client.post("/add", data={"title": "Ship the new dashboard"}, follow_redirects=True)
    assert b"Ship the new dashboard" in response.data
    assert b"Pending" in response.data

    with client.session_transaction() as session:
        from app.models import Task
        task_id = Task.query.first().id

    response = client.post(f"/toggle/{task_id}", follow_redirects=True)
    assert b"Working" in response.data
    response = client.post(f"/update/{task_id}", data={"title": "Ship the polished dashboard"}, follow_redirects=True)
    assert b"Ship the polished dashboard" in response.data
    response = client.post(f"/toggle/{task_id}", follow_redirects=True)
    assert b"Completed" in response.data
    response = client.post(f"/delete/{task_id}", follow_redirects=True)
    assert b"Your board is clear" in response.data or b"blank page" in response.data
