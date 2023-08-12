from fastapi import Depends, APIRouter, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List

from config.database import Session

from middlewares.auth_handler import JWTBearer

from schemas.todo import Todo
from schemas.list import TodoList

from services.list import ListService


list_router = APIRouter()


@list_router.get(path="/lists", tags=["list"], response_model=List[TodoList], status_code=200,
                 dependencies=[Depends(JWTBearer())])
def get_lists() -> JSONResponse:
    db = Session()
    service = ListService(db)

    result = service.get_lists()

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(result)
    )


@list_router.post(path="/lists", tags=["list"], response_model=TodoList, status_code=201,
                  dependencies=[Depends(JWTBearer())])
def create_list(todo_list: TodoList) -> JSONResponse:
    db = Session()
    service = ListService(db)

    service.create_list(todo_list)

    return JSONResponse(
        status_code=201,
        content=todo_list.model_dump()
    )


@list_router.get(path="/lists/{list_id}/todos", tags=["list"], response_model=List[Todo], status_code=200,
                 dependencies=[Depends(JWTBearer())])
def get_todos_for_list(list_id: int = Path(ge=1)):

    db = Session()
    service = ListService(db)

    result = service.get_todos(list_id)

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(result)
    )
