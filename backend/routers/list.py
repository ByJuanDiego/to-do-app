from fastapi import Depends, APIRouter, Path, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List, Annotated

from config.database import get_db, Session

from middlewares.auth_handler import jwt_bearer, oauth2_bearer

from schemas.user import User
from schemas.todo import Todo
from schemas.list import TodoList

from services.list import ListService
from services.user import UserService


list_router = APIRouter()


@list_router.post(path="/lists", tags=["list"], response_model=TodoList, status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(jwt_bearer)])
def create_list(todo_list: TodoList,
                current_user: Annotated[User, Depends(oauth2_bearer)],
                db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    user_service = UserService(db)
    user = user_service.get_user_by_username(todo_list.user_id)

    if not user_service.exists_user(user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found user with username {todo_list.user_id}!",
            headers={
                "Username-Conflict": todo_list.user_id
            }
        )

    if not user_service.has_same_username(current_user.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The requested user's username does not match the authenticated user's username. Access denied.",
            headers={
                "Username-Conflict": todo_list.user_id
            }
        )

    list_service = ListService(db)
    result = list_service.get_list_by_name(todo_list.name)

    if list_service.exists_list(result):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A list with name {todo_list.name} already exists!",
            headers={
                "Name-Conflict": todo_list.name
            }
        )

    list_service.create_list(todo_list)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=todo_list.model_dump())


@list_router.get(path="/list/{list_id}", tags=["list"], response_model=TodoList, status_code=status.HTTP_200_OK,
                 dependencies=[Depends(jwt_bearer)])
def get_list_by_id(list_id: Annotated[int, Path(ge=1)],
                   current_user: Annotated[User, Depends(oauth2_bearer)],
                   db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    list_service = ListService(db)
    todo_list = list_service.get_list_by_id(list_id)

    if not list_service.exists_list(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found list with id {list_id}!",
            headers={
                "Id-Conflict": str(list_id)
            }
        )

    user_service = UserService(db)
    user = todo_list.user

    if not user_service.has_same_username(current_user.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The requested user's username does not match the authenticated user's username. Access denied.",
            headers={
                "Username-Conflict": user.username
            }
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=TodoList.model_validate(todo_list).model_dump())


@list_router.get(path="/lists/{list_id}/todos", tags=["list"], response_model=List[Todo],
                 status_code=status.HTTP_200_OK, dependencies=[Depends(jwt_bearer)])
def get_todos_for_list(list_id: Annotated[int, Path(ge=1)],
                       current_user: Annotated[User, Depends(oauth2_bearer)],
                       db: Annotated[Session, Depends(get_db)]):
    list_service = ListService(db)
    todo_list = list_service.get_list_by_id(list_id)

    if not list_service.exists_list(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found list with id {list_id}!",
            headers={
                "Id-Conflict": str(list_id)
            }
        )

    user_service = UserService(db)
    user = todo_list.user

    if not user_service.has_same_username(current_user.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The requested user's username does not match the authenticated user's username. Access denied.",
            headers={
                "Username-Conflict": user.username
            }
        )

    if not list_service.has_any_todo(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No todo found in list with id {list_id}!",
            headers={
                "Id-Conflict": str(list_id)
            }
        )

    result = list_service.get_todos(list_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
