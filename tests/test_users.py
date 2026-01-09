import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_create_user(
    client
):
    response = client.post(
        "/users/", 
        json={
            "email": "test12345@gmail.com", 
            "password": "password123"
            }
        )
    new_user = schemas.UserOut(**response.json())

    assert new_user.email == "test12345@gmail.com"
    assert response.status_code==201

def test_login_user(
    client, 
    create_user
):
    user = create_user("user@test.com")
    response = client.post(
        "/login", 
        data={
            "username": user['email'],
            "password": user['password']
            }
        )

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    
    assert id == user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 404),
    ("test12345@gmail.com", "wrongPassword", 401)
])
def test_incorrect_login(
    client, 
    create_user, 
    email, 
    password, 
    status_code
):
    create_user("test12345@gmail.com")
    response = client.post(
        "/login", 
        data={
            "username": email, 
            'password': password}
        )

    assert response.status_code == status_code