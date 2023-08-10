from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field, EmailStr


from typing import Optional, List


from config.database import Session, Base, engine


from models.user import User as UserModel
from models.todo import Todo as TodoModel
from models.list import TodoList as TodoListModel


from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from middlewares.jwt_handler import signJWT


user_router = APIRouter()


class User(BaseModel):
    
    username : str = Field(max_length=100)

    password_hash : str = Field(max_length=100)

    email : Optional[EmailStr] = Field(max_length=100, default=None)

    name : Optional[str] = Field(max_length=100, default=None)

    class Config:

        json_schema_extra = {
            "examples": [
                {
                    "username": "ByJuanDiego",
                    "password_hash": "password",
                    "email": "juancaspadi@gmail.com",
                    "name": "Juan Diego"                    
                }
            ]
        }


def validate_unique_username(username: str) -> bool:
    db = Session()
    user = db.query(UserModel).get(username)
    return user is not None


def validate_unique_email(email:str) -> bool:
    db = Session()
    user = db.query(UserModel).filter(UserModel.email == email).first()
    return user is not None


def check_user(data: User) -> bool:

    db = Session()

    user = db.query(UserModel).get(data.username)

    if user is None:
        return False
    
    if user.password_hash == data.password_hash:
        return True

    return False


@user_router.post('/user/signup', tags=['user'], response_model=User, status_code=201)
def user_signup(user: User) -> User:
    

    if validate_unique_username(user.username):
        return JSONResponse(status_code=403, content={"error": "A user with this username already exists!"})

    elif validate_unique_email(user.email):
        return JSONResponse(status_code=403, content={"error": "A user with this email already exists!"})
    
    else:
        db = Session()

        new_user = UserModel(**user.dict())
        db.add(new_user)
        db.commit()

        return JSONResponse(status_code=201, content=user.dict())


@user_router.post('/user/login', tags=['user'], response_model=dict, status_code=200)
def user_login(user: User) -> str:

    if not check_user(user):
        return JSONResponse(status_code=404, content={"error": "Invalid username or password!"})

    return JSONResponse(status_code=200, content=signJWT(user.username))
