from fastapi import Depends, APIRouter, Path, HTTPException, status
from fastapi.responses import JSONResponse

from typing import Annotated

from config.database import get_db, Session

from middlewares.auth_handler import jwt_bearer, oauth2_bearer

from schemas.todo import Todo
from schemas.user import User

from services.todo import TodoService
from services.list import ListService
from services.user import UserService


todo_router = APIRouter()


@todo_router.post(path="/todos", tags=["todo"], response_model=Todo, status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(jwt_bearer)])
def create_todo(todo: Annotated[Todo, Depends()],
                current_user: Annotated[User, Depends(oauth2_bearer)],
                db: Annotated[Session, Depends(get_db)]) -> JSONResponse:

    list_service = ListService(db)
    todo_list = list_service.get_list_by_id(todo.list_id)

    if not list_service.exists_list(todo_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No list found with id {todo.list_id}!",
            headers={
                "Id-Conflict": str(todo.list_id)
            }
        )

    user = todo_list.user
    user_service = UserService(db)

    if not user_service.has_same_username(current_user.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The requested user's username does not match the authenticated user's username. Access denied.",
            headers={
                "Username-Conflict": user.username
            }
        )

    todo_service = TodoService(db)
    result = todo_service.get_todo_by_title_for_list(todo.title, todo.list_id)

    if todo_service.exists_todo(result):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A to-do with title {todo.title} already exists on list {todo_list.name}!",
            headers={
                "Title-Conflict": todo.title
            }
        )

    todo_service.create_todo(todo)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=todo.model_dump())


@todo_router.get(path="/todos/{todo_id}", tags=["todo"], response_model=Todo, status_code=status.HTTP_200_OK,
                 dependencies=[Depends(jwt_bearer)])
def get_todo_by_id(todo_id: Annotated[int, Path(ge=1)],
                   current_user: Annotated[User, Depends(oauth2_bearer)],
                   db: Annotated[Session, Depends(get_db)]) -> JSONResponse:

    todo_service = TodoService(db)
    todo = todo_service.get_todo_by_id(todo_id)

    if not todo_service.exists_todo(todo):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No todo found with id {todo_id}!",
            headers={
                "Id-Conflict": str(todo_id)
            }
        )

    user_service = UserService(db)
    user = todo.todo_list.user

    if not user_service.has_same_username(current_user.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The requested user's username does not match the authenticated user's username. Access denied.",
            headers={
                "Username-Conflict": user.username
            }
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=Todo.model_validate(todo).model_dump())
