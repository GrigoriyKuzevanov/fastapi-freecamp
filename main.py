from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default True if not in request body
    rating: int | None = None  # default = None if not in request body


MY_POSTS = [
        {"title": "title of post 1", "content": "content of post 1", "id": 1},
        {"title": "favorite foods", "content": "I like pizza", "id": 2},
    ]


def find_post(id: int, db: list):
    for item in db:
        if item["id"] == id:
            return item


def find_index_post(id: int, db: list):
    for i, post in enumerate(db):
        if post["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": MY_POSTS}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post(post_id, MY_POSTS)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} was not found")
    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    MY_POSTS.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    index = find_index_post(post_id, MY_POSTS)
    MY_POSTS.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
