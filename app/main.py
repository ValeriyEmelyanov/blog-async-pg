import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.db import database
from app.routes import users, posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def read_root():
    return {"message": "Hello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
