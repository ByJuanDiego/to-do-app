from fastapi import APIRouter, HTTPException, Depends, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from typing import Dict, List, Annotated


from config.database import Session

from utils.jwt_handler import sign_jwt

from schemas.user import UserRegistration, User
from schemas.list import TodoList

from services.user import UserService

from middlewares.auth_handler import oauth2_bearer, jwt_bearer


user_router = APIRouter()


@user_router.post(path="/users/signup", tags=["user"], response_model=UserRegistration,
                  status_code=status.HTTP_201_CREATED)
def user_signup(user: UserRegistration) -> JSONResponse:
    db = Session()
    service = UserService(db)

    result = service.get_user_by_username(user.username)

    if service.exists_user(result):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with username {user.username} already exists!",
            headers={
                "Username-Conflict": user.username
            }
        )

    elif service.exists_user_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with email {user.email} already exists!",
            headers={
                "Email-Conflict": user.email
            }
        )

    service.create_user(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump(exclude={"password_hash"}))


@user_router.post(path="/users/login", tags=["user"], response_model=Dict[str, str], status_code=status.HTTP_200_OK)
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:
    db = Session()
    service = UserService(db)

    result = service.get_user_by_username(form_data.username)

    if not service.exists_user(result):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found user with username {form_data.username}!",
            headers={
                "Username-Conflict": form_data.username
            }
        )

    if not service.validate_credentials(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password!",
            headers={
                "Username-Conflict": form_data.username
            }
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=sign_jwt(form_data.username))


@user_router.get(path="/users/{user_id}/lists", tags=["user"], response_model=List[TodoList],
                 dependencies=[Depends(jwt_bearer)])
def get_lists_for_user(user_id: Annotated[str, Path(max_length=100)],
                       current_user: Annotated[User, Depends(oauth2_bearer)]) -> JSONResponse:
    db = Session()
    service = UserService(db)

    user = service.get_user_by_username(user_id)

    if not service.exists_user(user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found user with username {user_id}!",
            headers={
                "Username-Conflict": user_id
            }
        )

    if not service.has_same_username(current_user.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The requested user's username does not match the authenticated user's username. Access denied.",
            headers={
                "Username-Conflict": user_id
            }
        )

    if not service.has_any_list(user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found any list for user {user_id}!",
            headers={
                "Username-Conflict": user_id
            }
        )

    lists: List[TodoList] = service.get_lists(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(lists))
