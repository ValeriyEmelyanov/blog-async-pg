from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db import users
from app.model.users import User, UserCreate, UserWithToken, TokenBase
from .users_dependencies import get_current_user

router = APIRouter()


@router.post("/signup", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    db_user = await users.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return await users.create_user(user)


@router.post("/auth", response_model=TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await users.get_user_by_email(email=form_data.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    if not users.validate_password(password=form_data.password, hashed_password=db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    db_token = await users.create_user_token(user_id=db_user["id"])
    return {
        "token": db_token["token"],
        "expires": db_token["expires"],
        "token_type": "bearer"
    }


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
