from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from enum import Enum

class VoteDir(int, Enum):
    REMOVE = 0
    UPVOTE = 1

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    Votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    

class Vote(BaseModel):
    post_id: int
    dir: VoteDir
