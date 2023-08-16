from typing import List

from config.database import Session

from models.user import User as UserModel
from models.list import TodoList as TodoListModel

from schemas.list import TodoList
from schemas.todo import Todo


class ListService:

    def __init__(self, database: Session) -> None:
        self.db: Session = database

    def __del__(self):
        self.db.close()

    @staticmethod
    def exists_list(todo_list: TodoListModel | None) -> bool:
        return todo_list is not None

    @staticmethod
    def exists_any_list(todo_lists: List[TodoListModel]) -> bool:
        return len(todo_lists) > 0

    @staticmethod
    def has_any_todo(todo_list: TodoListModel | None) -> bool:
        if todo_list is None:
            return False
        return len(todo_list.todos) > 0

    @staticmethod
    def get_user_for_list(todo_list: TodoListModel | None) -> UserModel | None:
        if todo_list is None:
            return None
        return todo_list.user

    def get_list_by_id(self, list_id: int) -> TodoListModel | None:
        todo_list = self.db.query(TodoListModel).get(list_id)
        return todo_list

    def get_list_by_name(self, list_name: str) -> TodoListModel | None:
        todo_list = self.db.query(TodoListModel).filter_by(name=list_name).first()
        return todo_list

    def get_lists(self):
        lists = self.db.query(TodoListModel).all()
        return lists

    def get_todos(self, list_id: int) -> List[Todo]:
        todo_list: TodoListModel | None = self.get_list_by_id(list_id)
        if not self.exists_list(todo_list):
            return []
        return todo_list.todos

    def create_list(self, todo_list: TodoList) -> None:
        new_todo_list = TodoListModel(**todo_list.model_dump())
        self.db.add(new_todo_list)
        self.db.commit()
