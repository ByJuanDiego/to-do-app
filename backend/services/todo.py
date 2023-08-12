from models.todo import Todo as TodoModel
from schemas.todo import Todo
from config.database import Session


class TodoService:

    def __init__(self, db: Session):
        self.db: Session = db

    def get_todos(self):
        todos = self.db.query(TodoModel).all()
        return todos

    def get_todo_by_id(self, todo_id: int) -> TodoModel | None:
        todo = self.db.query(TodoModel).get(todo_id)
        return todo

    def create_todo(self, todo: Todo) -> None:
        new_todo = TodoModel(**todo.model_dump())
        self.db.add(new_todo)
        self.db.commit()

    @staticmethod
    def exists_todo(todo_model: TodoModel | None) -> bool:
        return todo_model is not None
