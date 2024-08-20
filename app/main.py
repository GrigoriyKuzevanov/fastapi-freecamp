from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
from .database import engine
from . import models
from .routers import posts, users, auth, votes
from .config import settings


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API"}
