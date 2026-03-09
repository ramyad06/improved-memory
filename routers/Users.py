from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from database.db import SessionLocal
from models.todomodel import Todos,Users
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix = '/user',
    tags = ['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserVerification(BaseModel):
    password: str
    new_password:str = Field(min_length=6)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(user.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, User_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(User_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(User_verification.new_password)

    db.add(user_model)
    db.commit()