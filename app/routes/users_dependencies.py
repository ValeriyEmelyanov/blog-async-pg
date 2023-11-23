from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import app.db.users as users
import app.model.users as user_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> user_model.User:
    db_user = await users.get_user_by_token(token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_dict = {"id": db_user["id"], "email": db_user["email"], "name": db_user["name"]}
    return user_model.User(**user_dict)
