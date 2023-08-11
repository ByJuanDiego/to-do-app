from models.list import TodoList as TodoListModel
from schemas.list import TodoList
from config.database import Session


class ListService:

    def __init__(self, database: Session) -> None:
        self.db: Session = database

    def get_lists(self):
        lists = self.db.query(TodoListModel).all()
        return lists

    def create_list(self, todo_list: TodoList):
        new_todo_list = TodoListModel(**todo_list.model_dump())
        self.db.add(new_todo_list)
        self.db.commit()
