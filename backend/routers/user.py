from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from config.database import Session
from utils.jwt_handler import sign_jwt

from schemas.user import User
from services.user import UserService

user_router = APIRouter()


@user_router.post('/user/signup', tags=['user'], response_model=User, status_code=201)
def user_signup(user: User) -> JSONResponse:
    db = Session()

    if UserService(db).validate_unique_username(user.username):
        return JSONResponse(status_code=403, content={"error": "A user with this username already exists!"})

    elif UserService(db).validate_unique_email(user.email):
        return JSONResponse(status_code=403, content={"error": "A user with this email already exists!"})

    else:
        UserService(db).create_user(user)
        return JSONResponse(status_code=201, content=user.model_dump())


@user_router.post('/user/login', tags=['user'], response_model=Dict[str, str], status_code=200)
def user_login(user: User) -> JSONResponse:
    db = Session()
    if not UserService(db).validate_login(user.username, user.password_hash):
        return JSONResponse(status_code=404, content={"error": "Invalid username or password!"})

    return JSONResponse(status_code=200, content=sign_jwt(user.username))

