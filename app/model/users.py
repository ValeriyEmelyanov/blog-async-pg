# Для использования типа EmailStr необходимо установить модуль email-validator:
# pip install email-validator

from pydantic import BaseModel, EmailStr, UUID4, Field, field_validator
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """ Проверяет sign-up запрос """
    name: str
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    name: str


class TokenBase(BaseModel):
    # устанавливает псевдоним access_token для поля token;
    # lля обозначения, что поле обязательно,
    # в качестве первого параметра передается специальное значение — ... (ellipsis)
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        populate_by_name = True

    @field_validator("token")
    def hexlify_token(cls, value):
        """ Конвертирует UUID в hex строку """
        return value.hex


class UserWithToken(User):
    """ Формирует тело ответа с деталями пользователя и токеном """
    token: TokenBase = {}
