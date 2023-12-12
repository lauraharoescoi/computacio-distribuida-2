from typing import List
from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    username: str
    password: str
    token: str

class UserCreate(UserBase):
    username: str
    password: str


