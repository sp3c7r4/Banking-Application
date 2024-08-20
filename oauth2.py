from httplib2 import Credentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import jwt
import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

#Pieces of information that the token needs
#SECRET_KEY -> TO verifiy the integrity of a data
# Algorithm -> Hashing algorithm
#Expiration time -> TIme to expire

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encode_jwt

def verify_access_token(Token: str, credentials_exception):
  try:
    payload = jwt.decode(Token, SECRET_KEY, algorithms=[ALGORITHM])
    id: str = payload.get("user_id")
    if id is None:
      raise credentials_exception
    token_data = schemas.TokenData(id=id)
  except JWTError as e:
    raise credentials_exception
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Couldn't validate credentials", headers={"WWW-Authenticate":"Bearer"})
   return verify_access_token(token, credentials_exception)