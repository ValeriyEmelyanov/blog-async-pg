from fastapi import APIRouter, Depends, HTTPException, status

from app.model.posts import PostRequest, Post
from app.model.users import User
from app.db import posts
from .users_dependencies import get_current_user

router = APIRouter(prefix="/posts")


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_dict: PostRequest, current_user: User = Depends(get_current_user)):
    post_dict = await posts.create_post(post_dict, current_user)
    return post_dict


@router.get("/")
async def get_posts(page: int = 1):
    total_count = await posts.get_posts_count()
    posts_ = await posts.get_posts(page)
    return {"total_count": total_count, "result": posts_}


@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int):
    db_post = await posts.get_post(post_id)
    return {
        "id": db_post["id"],
        "title": db_post["title"],
        "user_name": db_post["user_name"],
        "created_at": db_post["created_at"],
        "content": db_post["content"]
    }


@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post_data: PostRequest, current_user=Depends(get_current_user)):
    db_post = await posts.get_post(post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id={post_id} does not exists"
        )
    if db_post["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this post"
        )
    await posts.update_post(post_id=post_id, post=post_data)
    return await get_post(post_id)
