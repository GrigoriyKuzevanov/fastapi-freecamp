import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    posts = [schemas.PostOutVotes(**post) for post in response.json()]

    assert len(posts) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client):
    response = authorized_client.get(f"/posts/10000")

    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOutVotes(**response.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("test-title", "test-content", True),
    ("test-2-title", "test-2-content", False),
    ("test-3-title", "test-3-content", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostOut(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user.get("id")


def test_create_post_default_published_true(authorized_client):
    response = authorized_client.post("/posts/", json={"title": "test-title", "content": "test-content"})

    created_post = schemas.PostOut(**response.json())

    assert response.status_code == 201
    assert created_post.published == True


def test_unauthorized_user_create_post(client):
    response = client.post("/posts/", json={"title": "test-title", "content": "test-content"})

    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert response.status_code == 204


def test_delete_post_non_exist(authorized_client):
    response = authorized_client.delete("/posts/100000")

    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[-1].id}")

    assert response.status_code == 403


def test_update_post(authorized_client, test_posts):
    data_to_update = {
        "title": "updated title",
        "content": "updated content",
    }

    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data_to_update)

    updated_post = schemas.PostOut(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data_to_update.get("title")
    assert updated_post.content == data_to_update.get("content")


def test_update_other_user_post(authorized_client, test_posts):
    data_to_update = {
        "title": "updated title",
        "content": "updated content",
    }

    response = authorized_client.put(f"/posts/{test_posts[-1].id}", json=data_to_update)

    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    data_to_update = {
        "title": "updated title",
        "content": "updated content",
    }
    response = client.put(f"/posts/{test_posts[0].id}", json=data_to_update)

    assert response.status_code == 401


def test_update_post_non_exist(authorized_client):
    data_to_update = {
        "title": "updated title",
        "content": "updated content",
    }
    response = authorized_client.put("/posts/100000", json=data_to_update)

    assert response.status_code == 404
