from .database import Base

class Posts(Base):
  __tablename__ = "posts"
  id: int