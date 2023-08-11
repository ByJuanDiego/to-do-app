from config.database import Session

from models.list import TodoList as TodoListModel

from schemas.list import TodoList


class ListService:

    def __init__(self, database: Session) -> None:
        self.db: Session = database

    def get_lists(self):
        lists = self.db.query(TodoListModel).all()
        return lists

    def get_todos(self, list_id: int):
        todo_list = self.db.query(TodoListModel).get(list_id)
        todos = todo_list.todos
        return todos

    def create_list(self, todo_list: TodoList) -> None:
        new_todo_list = TodoListModel(**todo_list.model_dump())
        self.db.add(new_todo_list)
        self.db.commit()

