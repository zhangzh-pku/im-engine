from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Boolean, JSON


Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    create_at = Column(DateTime, nullable=False)
    hashed_password = Column(String, nullable=False)

class FriendTable(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    friend_ids = Column(ARRAY(Integer), nullable=False)

class MessageTable(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, nullable=False)
    thread_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_read = Column(Boolean, nullable=False)
    reaction_counts = Column(JSON, nullable=False)
    reply_to_id = Column(Integer, nullable=True)
    reply_to_content = Column(String, nullable=True)
    edited_at = Column(DateTime, nullable=True)

class ReactionTable(Base):
    __tablename__ = "reactions"

    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    reaction_type = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)


class ThreadTable(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    owner_id = Column(Integer, nullable=False)
    admins = Column(ARRAY(Integer), nullable=False)
    members = Column(ARRAY(Integer), nullable=False)
    is_deleted = Column(Boolean, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    last_message_id = Column(Integer, nullable=True)
    last_message_content = Column(String, nullable=True)
    last_message_created_at = Column(DateTime, nullable=True)
    last_message_sender_id = Column(Integer, nullable=True)
    last_message_sender_name = Column(String, nullable=True)

