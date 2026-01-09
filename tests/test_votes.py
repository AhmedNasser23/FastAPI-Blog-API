import pytest
from app import models

def test_vote_on_another_user_post(
    authorized_client_factory, 
    create_posts, create_user
):
    user1 = create_user("user1@test.com")
    user2 = create_user("user2@test.com")
    user2_posts = create_posts(user2['id'])
    auth_client = authorized_client_factory(user1['id'])

    response = auth_client.post(
        "/vote/", 
        json={
        "post_id": user2_posts[0]['id'],
        "dir": 1}
    )

    assert response.status_code == 201

def test_vote_on_his_own_post(
    authorized_client_factory, 
    create_posts, 
    create_user
):
    user = create_user("user@test.com")
    auth_client = authorized_client_factory(user['id'])
    posts = create_posts(user['id'])

    response = auth_client.post(
        "/vote/", 
        json={
        "post_id": posts[0]['id'], 
        "dir": 1}
    )

    assert response.status_code == 403

def test_vote_on_voted_post(
    post_with_non_owner_client
):
    client = post_with_non_owner_client["client"]
    post = post_with_non_owner_client["post"]

    response = client.post(
        "/vote/",
        json={"post_id": post["id"], "dir": 1}
    )
    assert response.status_code == 201

    response = client.post(
        "/vote/",
        json={"post_id": post["id"], "dir": 1}
    )
    assert response.status_code == 409

def test_delete_vote(
    post_with_non_owner_client
):
    client = post_with_non_owner_client['client']
    post_id = post_with_non_owner_client['post']['id']

    client.post(
        "/vote/",
        json={
            "post_id": post_id,
            "dir": 1
        }
    )

    response = client.post(
        "/vote/", json={
            "post_id": post_id,
            "dir": 0
        }
    )

    assert response.status_code == 201

def test_delete_vote_not_exists(
    post_with_non_owner_client
):
    client = post_with_non_owner_client['client']
    post_id = post_with_non_owner_client['post']['id']

    response = client.post(
        "/vote/",
        json={
            "post_id": post_id,
            "dir": 0
        }
    )

    assert response.status_code == 404

def test_vote_unauthorized_user(client):
    response = client.post(
        "/vote/",
        json={
            "post_id": 1,
            "dir": 1
        }
    )

    assert response.status_code == 401