from fastapi import Body, FastAPI
#Initialization
app = FastAPI()

'''
Installation
pip install fastapi[all] -Installs all packages that works with fastApi
'''

#Defining a Route
  #Decorator - Turns a function into an api usable function
@app.get("/")
  #Function
def root():
  return {"message":"Hello World"} #Response - {"message":"Hello World"}

#Running the application 
#Uvicorn is a lightning-fast ASGI server implementation, using uvloop and httptools. E.g uvicorn main:app --reload (To run ur app, the reload flag checks your code and reloads your server  when there's changes in your code)
'''
Path Operation

@app.get("/") -> Decorator
  .get -> Method(For retrieving data)
  ("/") -> Path
  def root() -> Function
'''
@app.get("/posts")
def get_posts():
  return {"data":"This is your posts"}

#POST Requests
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
  print(payload)
  return {"data":f"title: {payload['title']} created successfully\n content: {payload['content']}"} 