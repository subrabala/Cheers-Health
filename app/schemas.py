from pydantic import BaseModel
from datetime import datetime


class NewPost(BaseModel):
    title: str
    content: str
    published: bool = True


class ResponseAccount(BaseModel):
    email: str
    hashed_password: str
    created_at: datetime

    class Config:
        orm_mode = True
