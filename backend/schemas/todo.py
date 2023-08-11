from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str = Field(max_length=60)

    description: str = Field(max_length=400)

