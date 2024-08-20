from passlib.context import CryptContext

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):      
  return pwd_content.hash(password)

def verify(plaintext_password, encrypted):
  return pwd_content.verify(plaintext_password, encrypted)

