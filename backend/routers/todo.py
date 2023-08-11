from fastapi import Depends, APIRouter, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List

from config.database import Session

from services.todo import TodoService

from middlewares.auth_handler import JWTBearer

from schemas.todo import Todo


todo_router = APIRouter()


@todo_router.get(path="/todo", tags=["todo"], response_model=List[Todo], status_code=200,
                 dependencies=[Depends(JWTBearer())])
def get_todos() -> JSONResponse:
    db = Session()

    result = TodoService(db).get_todos()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@todo_router.get(path="/todo/{todo_id}", tags=["todo"], response_model=Todo, status_code=200,
                 dependencies=[Depends(JWTBearer())])
def get_todo_by_id(todo_id: int = Path(ge=1)) -> JSONResponse:
    db = Session()

    result = TodoService(db).get_todo_by_id(todo_id)
    if result is None:
        return JSONResponse(status_code=404, content={"error": "Oops, to-do not found!"})

    return JSONResponse(status_code=200, content=Todo.model_validate(result).model_dump())


@todo_router.post(path="/todo", tags=["todo"], response_model=Todo, status_code=201,
                  dependencies=[Depends(JWTBearer())])
def create_todo(todo: Todo) -> JSONResponse:
    db = Session()
    TodoService(db).create_todo(todo)
    return JSONResponse(status_code=201, content=todo.model_dump())

