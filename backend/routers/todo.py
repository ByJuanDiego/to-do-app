from fastapi import Depends, APIRouter, Path, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List, Annotated

from config.database import get_db, Session

from middlewares.auth_handler import jwt_bearer, oauth2_bearer

from schemas.todo import Todo
from schemas.user import User

from services.todo import TodoService
from services.user import UserService


todo_router = APIRouter()


# TODO: Modify the endpoint to only get to-dos related to a specific list
@todo_router.get(path="/todos", tags=["todo"], response_model=List[Todo], status_code=status.HTTP_200_OK,
                 dependencies=[Depends(jwt_bearer)])
def get_todos(db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    service = TodoService(db)

    todos = service.get_todos()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(todos)
    )


@todo_router.post(path="/todos", tags=["todo"], response_model=Todo, status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(jwt_bearer)])
def create_todo(todo: Todo, db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    service = TodoService(db)
    # TODO: Create validation logic (403, 401, 409)
    service.create_todo(todo)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=todo.model_dump()
    )


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
