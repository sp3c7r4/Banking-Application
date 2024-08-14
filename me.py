from .database import engine
from . import models
from fastapi import FastAPI

app = FastAPI()
# Ensure all models are imported before calling create_all
models.Base.metadata.create_all(bind=engine)