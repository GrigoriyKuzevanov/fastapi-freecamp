import time
from random import randrange

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from . import models
from .database import engine
from .database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import schemas


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


MY_POSTS = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi_freecamp_db",
#             user="fastapi_freecamp_user",
#             password="fastapi_freecamp_password",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was succesful!")
#         break
#     except Exception as error:
#         print("Connecting to database faild")
#         print("Error: ", error)
#         time.sleep(2)


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


@app.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    stmt = select(models.Post)
    result = db.execute(stmt).all()
    posts = [row[0] for row in result]

    return posts


@app.get("/posts/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {post_id} was not found",
    #     )

    post = db.get(models.Post, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found",
        )
    
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put("/posts/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, post_id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    # if updated_post is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {post_id} was not found",
    #     )

    updated_post = db.get(models.Post, post_id)

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found",
        )

    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(updated_post, key, value)

    db.commit()
    db.refresh(updated_post)

    return updated_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # if deleted_post is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {post_id} was not found",
    #     )
    
    deleted_post = db.get(models.Post, post_id)

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found",
        )
    
    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
