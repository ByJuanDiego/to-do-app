from config.database import Base
from typing import List
import datetime

from sqlalchemy import (
    String, 
    TIMESTAMP,
    ForeignKey,
    func
    )

from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship
    )


class TodoList(Base):

    __tablename__ = "lists"


    id : Mapped[int] = mapped_column(primary_key=True)

    user_id : Mapped[int] = mapped_column(ForeignKey("users.username"))

    name : Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    
    registration_time : Mapped[datetime.datetime] = mapped_column(TIMESTAMP,  nullable=False, server_default=func.now())

    todos : Mapped[List["Todo"]] = relationship()
