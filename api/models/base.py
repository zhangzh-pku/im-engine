from sqlalchemy import (ARRAY, JSON, Boolean, Column, DateTime, ForeignKey,
                        Index, Integer, String, UniqueConstraint)
from sqlalchemy.orm import declarative_base

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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    friend_ids = Column(ARRAY(Integer), nullable=False)
    
    __table_args__ = (
        Index('idx_friends_user_id', user_id),
        Index('idx_friends_friend_ids', friend_ids, postgresql_using='gin'),
    )

class FriendRequestTable(Base):
    __tablename__ = "friend_requests"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    status = Column(Integer, nullable=False)
    __table_args__ = (
        Index("idx_user_friend", user_id, friend_id, unique=True),
        UniqueConstraint("user_id", "friend_id", name="unique_user_friend"),
    )
    

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

