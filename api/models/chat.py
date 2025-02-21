from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    id: int
    sender_id: int
    thread_id: int
    content: str
    created_at: datetime
    is_read: bool
    reaction_counts: dict[str, int]
    reply_to_id: int | None
    reply_to_content: str | None
    edited_at: datetime | None

class Reaction(BaseModel):
    message_id: int
    user_id: int
    reaction_type: int
    created_at: datetime

class Thread(BaseModel):
    id: int
    name: str
    created_at: datetime
    owner_id: int
    admins: list[int]
    members: list[int]