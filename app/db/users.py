import hashlib
import random
import string
from datetime import datetime, timedelta

from databases.core import Record
from sqlalchemy import and_

from app.model import users as user_model
from .db import database
from .users_schema import users_table, tokens_table


def get_random_string(length: int = 12) -> str:
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None) -> str:
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str) -> bool:
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_email(email: str) -> Record:
    """ Возвращает информацию о пользователе по email """
    query = (
        users_table.select()
        .where(users_table.c.email == email)
    )
    if not database.is_connected:
        await database.connect()
    return await database.fetch_one(query)


async def get_user_by_token(token: str) -> Record:
    """ Возвращает информацию о владельце указанного токена """
    query = (
        tokens_table.join(users_table)
        .select()
        .where(
            and_(
                tokens_table.c.token == token,
                tokens_table.c.expires > datetime.now()
            )
        )
    )
    if not database.is_connected:
        await database.connect()
    return await database.fetch_one(query)


async def create_user_token(user_id: int) -> Record:
    """ Создает токен для пользователя с указанным user_id """
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(hours=2), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )
    return await database.fetch_one(query)


async def create_user(user: user_model.UserCreate) -> dict:
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = (
        users_table.insert()
        .values(
            email=user.email,
            name=user.name,
            hashed_password=f"{salt}${hashed_password}"
        )
    )
    user_id = await database.execute(query)
    db_token = await create_user_token(user_id)
    token_dict = {"token": db_token["token"], "expires": db_token["expires"]}
    return {**user.model_dump(), "id": user_id, "is_active": True, "token": token_dict}
