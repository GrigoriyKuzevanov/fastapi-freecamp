import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app import database, models
from app.config import settings
from app.main import app
from app.oauth2 import create_access_token

DB_PORT = settings.db_port
DB_USER = settings.db_user
DB_NAME = settings.db_name
DB_HOST = settings.db_host
DB_PASSWORD = settings.db_password
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}_test"
)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:secret@localhost:5432/fastapi_freecamp_db_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test-user@mail.com",
        "password": "test-password",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user.get("id")})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }

    return client


@pytest.fixture
def test_posts(test_user: dict, test_user2: dict, session: Session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user.get("id"),
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user.get("id"),
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user.get("id"),
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2.get("id"),
        },
    ]

    posts_models = [models.Post(**post) for post in posts_data]

    session.add_all(posts_models)
    session.commit()

    posts = session.scalars(select(models.Post)).all()

    return posts


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "test-user2@mail.com",
        "password": "test-password2",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[1].id, user_id=test_user.get("id"))
    session.add(new_vote)
    session.commit()

