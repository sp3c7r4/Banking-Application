from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

'''
Why we Need Schema
+ It's a pain to get all the values from the body
+ The client can send what ever data they want
+ The data isn't getting Validated
+ We ultimately need to force the client to send data in a schema that we expect
'''


app= FastAPI()

class Post(BaseModel):
  title: str #title property, string - Data type
  content: str #content property, string - Data type
  published: bool = True
  rating: Optional[int] = None

@app.get('/')
def root():
  return "Hello"

#POST Requests
@app.post("/createposts")
def create_posts(newpost: Post):
  print(newpost.published, newpost.rating)
  print(newpost.model_dump())
  return {"data": newpost}

#We need a "title str", "content str", "category", "published bool" of a post