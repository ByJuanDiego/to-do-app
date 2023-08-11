from pydantic import BaseModel, Field, ConfigDict


class TodoList(BaseModel):

    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "name": "My to-do list",
                "user_id": "ByJuanDiego"
            }
        ]
    })

    name: str = Field(max_length=300)

    user_id: str = Field()
