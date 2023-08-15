from pydantic import BaseModel, Field, ConfigDict


class TodoList(BaseModel):

    name: str = Field(max_length=300)

    user_id: str = Field()

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "examples": [
            {
                "name": "My to-do list",
                "user_id": "ByJuanDiego"
            }
        ]
    })


class TodoListResponse(TodoList):

    registration_time: str = Field()

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "My to-do list",
                    "user_id": "ByJuanDiego",
                    "registration_time": "2023-08-15T10:44"
                }
            ]
        }
    )
