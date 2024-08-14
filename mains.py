from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
logger.info("Creating all tables in the database...")
models.Base.metadata.create_all(bind=engine)
logger.info("All tables created successfully.")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[str] = None
    published: bool = True
    id: int = None

# Database connection
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='spectra', 
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        logger.info("Database connection was successful!")
        break
    except Exception as err:
        logger.error(f"Connecting to Database Failed: {err}")
        time.sleep(2)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "I like pizza", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

app = FastAPI()

@app.get('/sqlalchemy')
def test_post(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/posts")
def posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get('/posts/{id}')
def root(id: int, response: Response):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100)
    my_posts.append(post_dict)
    return {"data": my_posts}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not Found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not Found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}