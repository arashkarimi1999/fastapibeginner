from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import session
from schemes import users as schemes
from models import users as models
from dependencies import get_db


router = APIRouter()

@router.post('/users/', response_model=schemes.User)
def create_user(user: schemes.UserCreate, db: session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Email already exists')
    user = models.User(
        email=user.email, username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/users/{user_id}', response_model=schemes.User)
def read(user_id: int, db: session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user
