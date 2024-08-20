from  .. import utils, schemas, models

app = APIRouter()

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
  try:
    new_user = models.User(email=user.email,password=utils.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

@app.get("/users/{id}", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
  getting = db.query(models.User).filter(models.User.id == id)
  getting_ok = getting.first()
  if not getting_ok:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
  return getting_ok