from contextlib import asynccontextmanager

import sqlalchemy
import uvicorn
from fastapi import FastAPI

from db.db import database
from db.posts import post_table
from db.users import users_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello world"}


@app.get("/posts")
async def read_posts():
    query = sqlalchemy.select([
        post_table.c.id,
        post_table.c.title,
        post_table.c.created_at,
        post_table.c.content,
        post_table.c.user_id,
        users_table.c.name.label("user_name"),
    ]).select_from(post_table.join(users_table)).order_by(sqlalchemy.desc(post_table.c.created_at))

    return await database.fetch_all(query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
