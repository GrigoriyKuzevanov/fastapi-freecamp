import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "hellos@mail.com", "password": "secret"}
    )
    new_user = schemas.UserOut(**response.json())

    assert new_user.email == "hellos@mail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login/",
        data={
            "username": test_user.get("email"),
            "password": test_user.get("password"),
        },
    )

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[
            settings.algorithm,
        ],
    )
    id = payload.get("user_id")

    assert id == test_user.get("id")
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@mail.com", "test-password", 403),
        ("test-user@mail.com", "wrongpassword", 403),
        ("wrongemail@mail.com", "wrongpassword", 403),
        (None, "test-password", 422),
        ("test-user@mail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login/", data={"username": email, "password": password})

    assert response.status_code == status_code
