from typing import List

from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from services.list import ListService

from config.database import Session
from middlewares.auth_handler import JWTBearer

list_router = APIRouter()


class TodoList(BaseModel):
    id: int = Field(ge=1)

    name: str = Field(max_length=300)

    user_id: int = Field(ge=1)


@list_router.get('/list', tags=['list'], response_model=List[TodoList], status_code=200,
                 dependencies=[Depends(JWTBearer())])
def get_lists() -> JSONResponse:

    db = Session()
    result = ListService(db).get_lists()

    return JSONResponse(status_code=200, content=jsonable_encoder(result))
