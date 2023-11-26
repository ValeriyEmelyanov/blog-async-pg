from datetime import datetime
from pydantic import BaseModel


class PostRequest(BaseModel):
    """ Validate request data """
    title: str
    content: str


class Post(BaseModel):
    """ Return response data """
    id: int
    title: str
    created_at: datetime
    user_name: str
    content: str
