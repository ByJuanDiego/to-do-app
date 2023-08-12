from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    username: str = Field(max_length=100)

    password_hash: str = Field(max_length=255)


class UserLogin(User):
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "username": "ByJuanDiego",
                "password_hash": "password"
            }
        ]
    })


class UserRegistration(User):
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "username": "ByJuanDiego",
                "password_hash": "password",
                "email": "juancaspadi@gmail.com",
                "name": "Juan Diego"
            }
        ]
    })

    email: EmailStr = Field(max_length=100)

    name: str = Field(max_length=100)
