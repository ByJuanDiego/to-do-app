from typing import Optional, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr

from config.database import Session
from utils.jwt_handler import sign_jwt
from models.user import User as UserModel

user_router = APIRouter()


class User(BaseModel):
    username: str = Field(max_length=100)

    password_hash: str = Field(max_length=100)

    email: Optional[EmailStr] = Field(max_length=100, default=None)

    name: Optional[str] = Field(max_length=100, default=None)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "username": "ByJuanDiego",
                    "password_hash": "password"
                }
            ]
        }


def validate_unique_username(username: str) -> bool:
    db = Session()
    user = db.query(UserModel).get(username)
    return user is not None


def validate_unique_email(email: str) -> bool:
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
def user_signup(user: User) -> JSONResponse:
    if validate_unique_username(user.username):
        return JSONResponse(status_code=403, content={"error": "A user with this username already exists!"})

    elif validate_unique_email(user.email):
        return JSONResponse(status_code=403, content={"error": "A user with this email already exists!"})

    else:
        db = Session()

        new_user = UserModel(**user.model_dump())
        db.add(new_user)
        db.commit()

        return JSONResponse(status_code=201, content=user.model_dump())


@user_router.post('/user/login', tags=['user'], response_model=Dict, status_code=200)
def user_login(user: User) -> JSONResponse:
    if not check_user(user):
        return JSONResponse(status_code=404, content={"error": "Invalid username or password!"})

    return JSONResponse(status_code=200, content=sign_jwt(user.username))
