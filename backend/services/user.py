from typing import List

from models.user import User as UserModel

from schemas.user import UserRegistration
from schemas.list import TodoList

from config.database import Session

from utils.hash_handler import get_hash, verify_password


class UserService:
    def __init__(self, db: Session):
        self.db: Session = db

    def __del__(self):
        self.db.close()

    def get_user_by_username(self, username: str) -> UserModel | None:
        user = self.db.query(UserModel).get(username)
        return user

    @staticmethod
    def exists_user(user: UserModel | None) -> bool:
        return user is not None

    @staticmethod
    def has_any_list(user: UserModel | None) -> bool:
        if user is None:
            return False
        return len(user.lists) > 0

    @staticmethod
    def has_same_username(username1: str, username2: str) -> bool:
        return username1 == username2

    @staticmethod
    def get_lists(user: UserModel | None) -> List[TodoList]:
        if user is None:
            return []
        return user.lists

    def exists_user_email(self, email: str) -> bool:
        user = self.db.query(UserModel).filter_by(email=email).first()
        return user is not None

    def validate_credentials(self, username: str, plain_password: str) -> bool:
        user = self.db.query(UserModel).get(username)

        if user is None:
            return False
        if verify_password(plain_password, user.password_hash):
            return True

        return False

    def create_user(self, user: UserRegistration) -> None:
        password_hash = get_hash(user.password_hash.get_secret_value())
        user.password_hash = password_hash

        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
