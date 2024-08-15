from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default True if not in request body


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True
