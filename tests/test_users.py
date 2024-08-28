from app import schemas
from .database import client, session


def test_root(client):
    response = client.get("/")
    print(response.json().get("message"))
    assert response.json().get("message") == "Welcome to my API"
    assert response.status_code == 200


def test_create_user(client):
    response = client.post("/users/", json={"email": "hellos@mail.com", "password": "secret"})
    new_user = schemas.UserOut(**response.json())

    assert new_user.email == "hellos@mail.com"
    assert response.status_code == 201
