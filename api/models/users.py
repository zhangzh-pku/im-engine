from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    create_at: datetime
    friend_ids: list[int]

class LoginRequest(BaseModel):
    name: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    password: str
    name: str

