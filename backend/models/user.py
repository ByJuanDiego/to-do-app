from config.database import Base
from typing import List
import datetime

from sqlalchemy import (
    String,
    TIMESTAMP,
    func
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False)

    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    registration_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    lists: Mapped[List["TodoList"]] = relationship()
