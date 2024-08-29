from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    posts = [schemas.PostOutVotes(**post) for post in response.json()]

    assert len(posts) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/10000")

    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOutVotes(**response.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
