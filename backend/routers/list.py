from fastapi import Depends, APIRouter, Path, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List, Annotated

from config.database import get_db, Session

from middlewares.auth_handler import jwt_bearer, oauth2_bearer

from schemas.todo import Todo
from schemas.list import TodoList

from services.list import ListService
from services.user import UserService


list_router = APIRouter()


@list_router.get(path="/lists", tags=["list"], response_model=List[TodoList], status_code=200,
                 dependencies=[Depends(jwt_bearer)])
def get_lists(db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    service = ListService(db)

    todo_lists = service.get_lists()

    if not service.exists_any_list(todo_lists):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not list was found!",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(todo_lists))


@list_router.post(path="/lists", tags=["list"], response_model=TodoList, status_code=201,
                  dependencies=[Depends(jwt_bearer)])
def create_list(todo_list: TodoList, db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
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


@list_router.get(path="/list/{list_id}", tags=["list"], response_model=TodoList, status_code=200,
                 dependencies=[Depends(jwt_bearer)])
def get_list_by_id(list_id: Annotated[int, Path(ge=1)], db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    service = ListService(db)

    todo_list = service.get_list_by_id(list_id)

    if not service.exists_list(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found list with id {list_id}!",
            headers={
                "Id-Conflict": str(list_id)
            }
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=todo_list)


@list_router.get(path="/lists/{list_id}/todos", tags=["list"], response_model=List[Todo],
                 status_code=status.HTTP_200_OK, dependencies=[Depends(jwt_bearer)])
def get_todos_for_list(list_id: Annotated[int, Path(ge=1)], db: Annotated[Session, Depends(get_db)]):
    service = ListService(db)

    todo_list = service.get_list_by_id(list_id)

    if not service.exists_list(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found list with id {list_id}!",
            headers={
                "Id-Conflict": str(list_id)
            }
        )

    if not service.has_any_todo(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No todo found in list with id {list_id}!",
            headers={
                "Id-Conflict": str(list_id)
            }
        )

    result = service.get_todos(list_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
