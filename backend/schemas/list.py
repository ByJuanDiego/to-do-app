from pydantic import BaseModel, Field


class TodoList(BaseModel):

    name: str = Field(max_length=300)

    user_id: str = Field()

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "My to-do list",
                    "user_id": "ByJuanDiego"
                }
            ]
        }
