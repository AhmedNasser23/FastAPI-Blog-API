import pytest
from typing import List
from app import schemas

def test_get_all_posts(
    create_user,
    authorized_client_factory,create_posts
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user["id"])
    posts = create_posts(user["id"])

    response = auth_client.get("/posts/")
    posts_list = list(map(lambda p: schemas.PostOut(**p), response.json()))

    assert response.status_code == 200
    assert len(posts_list) == len(posts)

def test_unauthorized_user_get_all_posts(
    client
):
    response = client.get('/posts/')
    assert response.status_code == 401

def test_unauthorized_user_one_post(
    client, 
    create_posts, 
    create_user
):
    user = create_user("user@test.com")
    posts = create_posts(user["id"])

    response = client.get(f"/posts/{posts[0]['id']}")
    assert response.status_code == 401

def test_get_one_post_not_exits(
    create_user, 
    authorized_client_factory
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user["id"])

    response = auth_client.get(f"/posts/{33}")
    assert response.status_code == 404

def test_get_one_post(
    create_user, 
    authorized_client_factory, 
    create_posts
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user['id'])
    posts = create_posts(user['id'])

    response = auth_client.get(f"/posts/{posts[0]['id']}")
    post = schemas.PostOut(**response.json())

    assert response.status_code == 200
    assert post.Post.id == posts[0]['id']

@pytest.mark.parametrize("title, content, published", [
    ("title 1", "content 1", True),
    ("title 2", "content 2", True),
    ("title 3", "content 3", True),
])
def test_create_post(
    create_user, 
    authorized_client_factory, 
    title, 
    content, 
    published
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user['id'])

    response = auth_client.post(
        "/posts/", 
        json={
            "title": title, 
            "content": content, 
            "published": published
            }
        )

    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.owner_id == user['id']

def test_create_post_default_true(
    create_user, 
    authorized_client_factory
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user['id'])

    response = auth_client.post(
        "/posts/", 
        json={
            "title": "title", 
            "content": "content"
            }
        )

    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.published == True

def test_unauthorized_user_create_post(
    client
):
    response = client.post(
        "/posts/", 
        json={
            "title": "title", 
            "content": "content"
            }
        )

    assert response.status_code == 401

def test_unauthorized_delete_post(
    client, 
    create_user, 
    create_posts
):
    user = create_user("user@test.com")
    posts = create_posts(user['id'])

    response = client.delete(f"/posts/{posts[0]['id']}")
    assert response.status_code == 401

def test_delete_post(
    create_user, 
    authorized_client_factory, 
    create_posts
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user["id"])
    posts = create_posts(user["id"])

    response = auth_client.delete(f"/posts/{posts[0]['id']}")
    remaining = auth_client.get(f"/posts/").json()

    assert response.status_code == 204
    assert len(remaining) == len(posts)-1

def test_delete_post_non_exist(
    create_user, 
    authorized_client_factory
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user['id'])
    
    response = auth_client.delete(f"/posts/{100}")
    assert response.status_code == 404

def test_delete_other_user_post(
    create_user, 
    authorized_client_factory, 
    create_posts
):
    user1 = create_user("user1@test.com")
    user2 = create_user("user2@test.com")

    user1_posts = create_posts(user1['id'])
    client2 = authorized_client_factory(user2['id'])

    response = client2.delete(f"/posts/{user1_posts[0]['id']}")

    assert response.status_code == 403

def test_update_post(
    create_user, 
    authorized_client_factory, 
    create_posts
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user['id'])
    posts = create_posts(user['id'])

    updated_post = {
        "title": "new title",
        "content": "new content",
        "id": posts[0]['id']
    }

    response = auth_client.put(
        f"/posts/{posts[0]['id']}", 
        json=updated_post
    )
    returned_post = schemas.Post(**response.json())
    
    assert response.status_code == 200
    assert returned_post.title == updated_post['title']

def test_update_other_user_post(
    create_user, 
    authorized_client_factory, 
    create_posts
):
    user1 = create_user("user1@test.com")
    user2 = create_user("user2@test.com")

    user1_posts = create_posts(user1['id'])
    client2 = authorized_client_factory(user2['id'])

    updated_post = {
        "title": "new title",
        "content": "new content",
        "id": user1_posts[0]['id']
    }

    response = client2.put(
        f"/posts/{user1_posts[0]['id']}", 
        json=updated_post
    )

    assert response.status_code == 403

def test_unauthorized_delete_post(
    client, 
    create_user, 
    create_posts
):
    user = create_user("user@test.com")
    posts = create_posts(user['id'])
    
    updated_post = {
        "title": "new title",
        "content": "new content",
        "id": posts[0]['id']
    }

    response = client.put(
        f"/posts/{posts[0]['id']}", 
        json=updated_post
    )

    assert response.status_code == 401

def test_update_post_not_exist(
    create_user, 
    authorized_client_factory, 
    create_posts
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user['id'])
    posts = create_posts(user['id'])

    updated_post = {
        "title": "new title",
        "content": "new content",
        "id": posts[0]['id']
    }

    response = auth_client.put(
        f"/posts/{100}", 
        json=updated_post
    )

    assert response.status_code == 404