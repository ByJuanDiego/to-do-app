from typing import List

from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from middlewares.auth_handler import JWTBearer

from schemas.list import TodoList
from services.list import ListService


list_router = APIRouter()


@list_router.get('/list', tags=['list'], response_model=List[TodoList], status_code=200,
                 dependencies=[Depends(JWTBearer())])
def get_lists() -> JSONResponse:

    db = Session()
    result = ListService(db).get_lists()

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@list_router.post('/list', tags=['list'], response_model=TodoList, status_code=201,
                  dependencies=[Depends(JWTBearer())])
def create_list(todo_list: TodoList) -> JSONResponse:

    db = Session()
    ListService(db).create_list(todo_list)

    return JSONResponse(status_code=201, content=todo_list.model_dump())
