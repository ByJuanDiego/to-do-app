from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from typing import Dict

from config.database import Session

from utils.jwt_handler import sign_jwt

from schemas.user import UserLogin, UserRegistration

from services.user import UserService


user_router = APIRouter()


@user_router.post(path="/users/signup", tags=["user"], response_model=UserRegistration, status_code=201)
def user_signup(user: UserRegistration) -> JSONResponse:
    db = Session()
    service = UserService(db)

    result = service.get_user_by_username(user.username)

    if service.exists_user(result):
        raise HTTPException(
            status_code=403,
            detail=f"A user with username {user.username} already exists!",
            headers={
                "Username-Conflict": user.username
            }
        )

    elif service.exists_user_email(user.email):
        raise HTTPException(
            status_code=403,
            detail=f"A user with email {user.email} already exists!",
            headers={
                "Email-Conflict": user.email
            }
        )

    service.create_user(user)
    return JSONResponse(
        status_code=201,
        content=user.model_dump(exclude={"password_hash"})
    )


@user_router.post(path="/users/login", tags=["user"], response_model=Dict[str, str], status_code=200)
def user_login(user: UserLogin) -> JSONResponse:
    db = Session()
    service = UserService(db)

    result = service.get_user_by_username(user.username)

    if not service.exists_user(result):
        raise HTTPException(
            status_code=403,
            detail=f"Not found user with username {user.username}!",
            headers={
                "Username-Conflict": user.username
            }
        )

    if not service.validate_credentials(user.username, user.password.get_secret_value()):
        raise HTTPException(
            status_code=403,
            detail="Invalid username or password!",
            headers={
                "Username-Conflict": user.username
            }
        )

    return JSONResponse(status_code=200, content=sign_jwt(user.username))
