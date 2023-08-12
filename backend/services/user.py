from models.user import User as UserModel
from schemas.user import User

from config.database import Session


class UserService:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.db.query(UserModel).get(username)

    @staticmethod
    def exists_user(user: UserModel | None) -> bool:
        return user is not None

    def exists_user_email(self, email: str) -> bool:
        user = self.db.query(UserModel).filter_by(email=email).first()
        return user is not None

    def validate_credentials(self, username: str, password_hash: str) -> bool:
        user = self.db.query(UserModel).get(username)

        if user is None:
            return False
        if user.password_hash == password_hash:
            return True

        return False

    def create_user(self, user: User) -> None:
        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
