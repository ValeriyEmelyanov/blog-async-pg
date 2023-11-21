from fastapi import APIRouter, HTTPException

from app.db import users
from app.model.users import User, UserCreate


router = APIRouter()


@router.post("/signup", response_model=User)
async def create_user(user: UserCreate):
    db_user = await users.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users.create_user(user)

