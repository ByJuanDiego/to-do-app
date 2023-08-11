import uvicorn

from fastapi import FastAPI

from middlewares.error_handler import ErrorHandler

from routers.user import user_router
from routers.list import list_router
from routers.todo import todo_router

# from config.database import Base, engine

app = FastAPI()

app.title = "To-Do App"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(list_router)
app.include_router(todo_router)

# Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
