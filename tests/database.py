from fastapi.testclient import TestClient
from app.main import app
from app import database
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


DB_PORT = settings.db_port
DB_USER = settings.db_user
DB_NAME = settings.db_name
DB_HOST = settings.db_host
DB_PASSWORD = settings.db_password
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}_test"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:secret@localhost:5432/fastapi_freecamp_db_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)