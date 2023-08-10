from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field, EmailStr


from typing import Optional, List


from config.database import Session, Base, engine


from models.user import User as UserModel
from models.todo import Todo as TodoModel
from models.list import TodoList as TodoListModel


from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from middlewares.jwt_handler import signJWT


list_router = APIRouter()


class TodoList(BaseModel):

    id : int = Field(ge=1)

    name : str = Field(max_length=300)

    user_id : int = Field(ge=1)


@list_router.get('/list', tags=['list'], response_model=List[TodoList], status_code=200, dependencies=[Depends(JWTBearer())])
def get_lists() -> List[TodoList]:

    db = Session()
    result = db.query(TodoListModel).all()

    return JSONResponse(status_code=200, content=jsonable_encoder(result))

