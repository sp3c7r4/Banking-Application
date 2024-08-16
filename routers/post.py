from  ..banking import schemas, models


app = APIRouter()

@app.get("/posts", response_model=List[schemas.Post])
def posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  # cursor.execute("SELECT * FROM posts")
  # posts = cursor.fetchall()
  return posts

@app.get('/posts/{id}')
def root(id: int, response: Response, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).first()
  # cursor.execute(f"SELECT * FROM posts WHERE id={id}")
  # posts = cursor.fetchone()
  # post = find_post(int(id))
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # response.status_code = status.HTTP_404_NOT_FOUND
  #   # return {'message': f"post with id: {id} was not found"}
  # print(post)
  return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
  my_posts = models.Post(**post.dict())
  db.add(my_posts)
  db.commit()
  db.refresh(my_posts)
  #cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ('{post.title}','{post.content}',{post.published}) RETURNING *")
  # my_posts = cursor.fetchone()
  # conn.commit()
  return my_posts

# def find_index_post(id):
#   for i, p in enumerate(my_posts):
#     if p['id'] == id:
#       return i
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id)
  # cursor.execute(f"DELETE FROM posts WHERE id={id} returning *")
  # index = cursor.fetchone()
  # conn.commit()
  #Deleting post
  #Find the index in the array that has Required ID
  #my_post.pop()
  #index = find_index_post(id)
  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not Found")
  post.delete(synchronize_session=False)
  db.commit()
  #my_posts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)
 
#Update
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, posts: schemas.PostCreate, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id==id)
  index = post_query.first()
  # cursor.execute(f"UPDATE posts SET title='{post.title}', content='{post.content}', published={post.published} WHERE id={id} returning *")
  # index = cursor.fetchone()
  # conn.commit()
  #index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not Found")
  post_query.update({'title':posts.title, 'content': posts.content},synchronize_session=False)
  db.commit()
  db.refresh(index)
  # post_dict = post.model_dump()
  # post_dict['id'] = id
  # my_posts[index] = post_dict
  return  index