import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app import models
from app.oauth2 import create_access_token
from urllib.parse import quote_plus

# Encode the password to handle special characters
password = quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:"
    f"{password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture
def client(
    session
):
    # the code will be run before our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db]= override_get_db
    yield TestClient(app)
    # the code will be run after our test

@pytest.fixture
def create_user(
    client
):
    def _create_user(email: str, password: str = "password123"):
        response = client.post(
            "/users/",
            json={"email": email, "password": password}
        )

        assert response.status_code == 201
        user = response.json()
        user["password"] = password
        return user
    return _create_user

@pytest.fixture
def create_token():
    def _create_token(user_id: int):
        return create_access_token({"user_id": user_id})
    return _create_token

@pytest.fixture
def authorized_client_factory(
    client, 
    create_token
):
    def _authorized_client(user_id: int):
        token = create_token(user_id)
        client.headers = {
            **client.headers,
            "Authorization": f"Bearer {token}"
        }
        return client
    return _authorized_client

@pytest.fixture
def create_posts(
    session
):
    def _create_posts(
        owner_id: int
    ):
        posts_data = [
            {"title": "first title", "content": "first content", "owner_id": owner_id},
            {"title": "second title", "content": "second content", "owner_id": owner_id},
            {"title": "third title", "content": "third content", "owner_id": owner_id},
        ]

        posts = list(map(lambda p: models.Post(**p), posts_data))
        session.add_all(posts)
        session.commit()
        return [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "owner_id": post.owner_id,
            }
            for post in posts
        ]

    return _create_posts

@pytest.fixture
def post_with_non_owner_client(
    create_user,
    create_posts,
    authorized_client_factory
):
    owner = create_user("owner@test.com")
    voter = create_user("voter@test.com")

    posts = create_posts(owner["id"])
    voter_client = authorized_client_factory(voter["id"])

    return {
        "owner": owner,
        "voter": voter,
        "post": posts[0],
        "client": voter_client
    }
