from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from constants.roles import Roles
import datetime
import re

class BaseUser(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length=8)
    passwordRepeat: str = Field(..., min_length=8, description='Пароли должны совпадать')
    roles: list[Roles] = [Roles.USER]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email должен быть корректным")
        return value

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value
