from pydantic import BaseModel, Field, EmailStr, ConfigDict, SecretStr


class User(BaseModel):
    username: str = Field(max_length=100)


class UserLogin(User):
    password: SecretStr = Field(max_length=255)

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "examples": [
            {
                "username": "ByJuanDiego",
                "password": "password"
            }
        ]
    })


class UserRegistration(User):
    password_hash: SecretStr = Field(max_length=255, alias="password")

    email: EmailStr = Field(max_length=100)

    name: str = Field(max_length=100)

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "examples": [
            {
                "name": "Juan Diego",
                "username": "ByJuanDiego",
                "email": "juancaspadi@gmail.com",
                "password": "password"
            }
        ]
    })
