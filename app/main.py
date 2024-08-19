from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
from .database import engine
from . import models
from .routers import posts, users, auth
from .config import settings


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


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


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API"}
