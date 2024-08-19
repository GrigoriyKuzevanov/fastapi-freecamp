from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default True if not in request body


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    owner_id: int
    created_at: datetime
    id: int
    owner: UserOut

    class Config:
        from_attributes = True
