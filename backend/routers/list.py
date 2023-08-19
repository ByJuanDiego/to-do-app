from fastapi import Depends, APIRouter, Path, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List, Annotated

from config.database import get_db, Session

from middlewares.auth_handler import jwt_bearer, oauth2_bearer

from schemas.user import User
from schemas.todo import Todo
from schemas.list import TodoList, TodoListResponse

from services.list import ListService
from services.user import UserService


list_router = APIRouter()


def authorize_list_access(list_id: int, current_user: User, list_service: ListService, user_service: UserService):
    todo_list = list_service.get_list_by_id(list_id)

    if not list_service.exists_list(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found list with id {list_id}!",
            headers={
                "Id-Conflict": str(list_id)
            }
        )

    user = list_service.get_user_for_list(todo_list)

    if not user_service.has_same_username(current_user.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The requested user's username does not match the authenticated user's username. Access denied.",
            headers={
                "Username-Conflict": user.username
            }
        )

    return todo_list


@list_router.post(path="/lists", tags=["list"], response_model=TodoList, status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(jwt_bearer)])
def create_list(todo_list: Annotated[TodoList, Depends()],
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


@list_router.get(path="/lists/{list_id}", tags=["list"], response_model=TodoListResponse, status_code=status.HTTP_200_OK,
                 dependencies=[Depends(jwt_bearer)])
def get_list_by_id(list_id: Annotated[int, Path(ge=1)],
                   current_user: Annotated[User, Depends(oauth2_bearer)],
                   db: Annotated[Session, Depends(get_db)]) -> JSONResponse:

    list_service = ListService(db)
    user_service = UserService(db)

    todo_list = authorize_list_access(list_id, current_user, list_service, user_service)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=TodoListResponse.model_validate(jsonable_encoder(todo_list)).model_dump())


@list_router.get(path="/lists/{list_id}/todos", tags=["list"], response_model=List[Todo],
                 status_code=status.HTTP_200_OK, dependencies=[Depends(jwt_bearer)])
def get_todos_for_list(list_id: Annotated[int, Path(ge=1)],
                       current_user: Annotated[User, Depends(oauth2_bearer)],
                       db: Annotated[Session, Depends(get_db)]):

    list_service = ListService(db)
    user_service = UserService(db)

    todo_list = authorize_list_access(list_id, current_user, list_service, user_service)

    if not list_service.has_any_todo(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Any todo found in list {todo_list.name}",
            headers={
                "Id-Conflict": str(todo_list.id)
            }
        )

    result = list_service.get_todos(list_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
