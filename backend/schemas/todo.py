from pydantic import BaseModel, Field, ConfigDict

from typing import Optional


class Todo(BaseModel):

    list_id: Optional[int] = Field(ge=1, default=None)

    title: str = Field(max_length=60)

    description: str = Field(max_length=400)

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
            "examples": [
                {
                    "list_id": 1,
                    "title": "Dormir más temprano",
                    "description": "Ya comienza el ciclo y todavía no regulo mi horario de sueño"
                }
            ]
        })
