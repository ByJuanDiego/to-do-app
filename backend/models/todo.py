from config.database import Base
import datetime

from sqlalchemy import (
    String,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    func
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id"))

    title: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)

    description: Mapped[str] = mapped_column(String(400), nullable=False)

    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    registration_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())

    todo_list: Mapped["TodoList"] = relationship(argument="TodoList", back_populates="todos")
