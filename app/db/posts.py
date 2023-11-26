from datetime import datetime
from sqlalchemy import desc, func, select
from databases.core import Record

from .db import database
from .posts_schema import post_table
from .users_schema import users_table
from app.model import posts as post_model
from app.model import users as user_model


async def create_post(post: post_model.PostRequest, user: user_model.User) -> dict:
    """ Создает новый пост в БД """
    query = (
        post_table.insert()
        .values(
            title=post.title,
            content=post.content,
            created_at=datetime.now(),
            user_id=user.id,
        )
        .returning(
            post_table.c.id,
            post_table.c.title,
            post_table.c.content,
            post_table.c.created_at,
        )
    )
    if not database.is_connected:
        await database.connect()
    db_post = await database.fetch_one(query)
    post = dict(zip(db_post, db_post.values()))
    post["user_name"] = user.name
    return post


async def get_post(post_id: int) -> Record:
    """ Возвращает информацию о посте по идентификатору """
    query = (
        select(
            [
                post_table.c.id,
                post_table.c.title,
                post_table.c.created_at,
                post_table.c.content,
                post_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(post_table.join(users_table))
        .where(post_table.c.id == post_id)
    )
    if not database.is_connected:
        await database.connect()
    return await database.fetch_one(query)


async def get_posts(page: int) -> list[Record]:
    """ Возвращает список постов для страницы с указанным номером, нумерация страниц с 1"""
    max_per_page = 10
    offset = (page - 1) * max_per_page
    query = (
        select(
            [
                post_table.c.id,
                post_table.c.title,
                post_table.c.created_at,
                post_table.c.content,
                post_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(post_table.join(users_table))
        .order_by(desc(post_table.c.created_at))
        .limit(max_per_page)
        .offset(offset)
    )
    if not database.is_connected:
        await database.connect()
    # return await database.fetch_all(query)
    return await database.fetch_all(query)


async def get_posts_count() -> int:
    """ Возвращает общее количество постов в БД """
    query = (
        select(
            [
                func.count()
            ]
        )
        .select_from(post_table)
    )
    if not database.is_connected:
        await database.connect()
    return await database.fetch_val(query)


async def update_post(post_id: int, post: post_model.PostRequest) -> None:
    """ Обновляет пост с указанным идентификатором """
    query = (
        post_table.update()
        .where(post_table.c.id == post_id)
        .values(
            title=post.title,
            content=post.content,
        )
    )
    if not database.is_connected:
        await database.connect()
    await database.execute(query)
