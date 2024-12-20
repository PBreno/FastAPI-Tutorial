from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
   pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostCreate):
    id: int
    created_at: datetime
    owner: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]
