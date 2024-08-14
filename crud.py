from sqlite3 import DatabaseError
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.background import P
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
'''
CRUD - Create Read Updte Delete
This is an acronym that represents the 4 main functions of an APPlication. So any application regardless of how it's created it should be able to create things, Read thingsm Update things. and Delete things


CREATE  ->  POST      /posts      @app.post("/post")
READ    ->  GET       /posts/:id  @app.get("/posts/{id}")
            GET       /posts      @app.get("/posts")
UPDATE  ->  PUT/PATCH /posts/:id  @app.put("/posts/{id}")
DELETE  ->  DELETE    /posts/:id  @app.delete("/posts/{id}")
'''

class Post(BaseModel):
  title: str
  content: str
  rating: Optional[str] = None
  published: bool = True
  id: int = None

while True:
  try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='spectra', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesful!")
    break
  except Exception as err:
    print("Connecting to Database Failed")
    print(f"Error: {err}")
    time.sleep(2)

app = FastAPI()

my_posts =  [
  {"title":"title of post 1", "content":"content of post 1", "id":1},
  {"title":"favourite foods", "content":"I like pizza", "id":2}
          ]

def find_post(id):
  for p in my_posts:
    if p["id"] == id:
      return p

@app.get("/posts")
def posts():
  cursor.execute("SELECT * FROM posts")
  posts = cursor.fetchall()
  return {"data": posts}
  pass

@app.get('/posts/{id}')
def root(id: int, response: Response):
  post = find_post(int(id))
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'message': f"post with id: {id} was not found"}
  print(post)
  return {"data": f"Here's the post id: {post}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  post_dict = post.model_dump()
  post_dict['id'] = randrange(0, 100)
  my_posts.append(post_dict)
  return {"data": my_posts}

def find_index_post(id):
  for i, p in enumerate(my_posts):
    if p['id'] == id:
      return i
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  #Deleting post
  #Find the index in the array that has Required ID
  #my_post.pop()
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not Found")
  my_posts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)



#Update
@app.put("/posts/{id}")
def update_post(id: int, post: Post, status_code=status.HTTP_200_OK):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not Found")
  post_dict = post.model_dump()
  post_dict['id'] = id
  my_posts[index] = post_dict
  return {"data": post_dict}
  pass