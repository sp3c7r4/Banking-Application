from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):
  pass

class Post(BaseModel):
  title: str
  content: str
  published: bool
  created_at: datetime
  id: int
  class Config:
        orm_mode = True

class UserCreate(BaseModel):
   email: EmailStr
   password: str

class UserOut(BaseModel):
  id: int
  email: EmailStr

class UserLogin(BaseModel):
   email: EmailStr
   password: Optional[str] = 'me'

class Token(BaseModel):
   access_token: str
   token_type: str

class TokenData(BaseModel):
   id: Optional[str] = None