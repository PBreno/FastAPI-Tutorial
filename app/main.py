import time
import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from .routers import post, user
from . import models
from app.database import engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connect!")
        break
    except Exception as e:
        print(e)
        time.sleep(3)


app.include_router(post.router)
app.include_router(user.router)
@app.get("/")
def root():
    return {"message": "Hello World"}




