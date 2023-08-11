from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class User(BaseModel):
    username: str = Field(max_length=100)

    password_hash: str = Field(max_length=100)

    email: Optional[EmailStr] = Field(max_length=100, default=None)

    name: Optional[str] = Field(max_length=100, default=None)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "username": "ByJuanDiego",
                    "password_hash": "password"
                }
            ]
        }
