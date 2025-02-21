from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    create_at: datetime
    friend_ids: list[int]

