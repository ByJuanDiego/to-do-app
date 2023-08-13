from fastapi import Depends, APIRouter, Path, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List, Annotated

from config.database import get_db, Session

from middlewares.auth_handler import jwt_bearer

from schemas.todo import Todo

from services.todo import TodoService


todo_router = APIRouter()


@todo_router.get(path="/todos", tags=["todo"], response_model=List[Todo], status_code=200,
                 dependencies=[Depends(jwt_bearer)])
def get_todos(db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    service = TodoService(db)

    todos = service.get_todos()

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(todos)
    )


@todo_router.post(path="/todos", tags=["todo"], response_model=Todo, status_code=201,
                  dependencies=[Depends(jwt_bearer)])
def create_todo(todo: Todo, db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    service = TodoService(db)

    service.create_todo(todo)

    return JSONResponse(
        status_code=201,
        content=todo.model_dump()
    )


@todo_router.get(path="/todos/{todo_id}", tags=["todo"], response_model=Todo, status_code=200,
                 dependencies=[Depends(jwt_bearer)])
def get_todo_by_id(todo_id: Annotated[int, Path(ge=1)], db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    service = TodoService(db)

    todo = service.get_todo_by_id(todo_id)

    if not service.exists_todo(todo):
        raise HTTPException(
            status_code=404,
            detail=f"No todo found with id {todo_id}!",
            headers={
                "Id-Conflict": str(todo_id)
            }
        )

    return JSONResponse(status_code=200, content=Todo.model_validate(todo).model_dump())
