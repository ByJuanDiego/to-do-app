from models.list import TodoList
from config.database import Session


class ListService:

    def __init__(self, database: Session) -> None:
        self.database: Session = database

    def get_lists(self):
        lists = self.database.query(TodoList).all()
        return lists
