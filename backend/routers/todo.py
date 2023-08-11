from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
#
# from pydantic import BaseModel, Field
#
# from typing import Optional, List
#
# from config.database import Session, Base, engine
#
# from models.user import User as UserModel
# from models.todo import Todo as TodoModel
# from models.list import TodoList as TodoListModel
#
# from middlewares.auth_handler import JWTBearer
#
todo_router = APIRouter()
#
#
