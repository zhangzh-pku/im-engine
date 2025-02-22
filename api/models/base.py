from sqlalchemy import (ARRAY, JSON, Boolean, Column, DateTime, ForeignKey,
                        Index, Integer, String, UniqueConstraint)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    create_at = Column(DateTime, nullable=False)
    phone_number = Column(String, nullable=True)
    handle = Column(String, nullable=True)

class FriendTable(Base):
    __tablename__ = "friends"

    user_id = Column(Integer, nullable=False, primary_key=True)
    friend_ids = Column(ARRAY(Integer), nullable=False)
    
    __table_args__ = (
        Index('idx_friends_user_id', user_id),
        Index('idx_friends_friend_ids', friend_ids, postgresql_using='gin'),
    )

class FriendRequestTable(Base):
    __tablename__ = "friend_requests"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,  nullable=False)
    friend_id = Column(Integer,  nullable=False)
    status = Column(Integer, nullable=False)
    __table_args__ = (
        Index("idx_user_friend", user_id, friend_id, unique=True),
        UniqueConstraint("user_id", "friend_id", name="unique_user_friend"),
    )
    

class MessageTable(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, nullable=False)
    thread_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_read = Column(Boolean, nullable=False)
    reaction_counts = Column(JSON, nullable=False)
    reply_to_message_id = Column(Integer, nullable=True)
    edited_at = Column(DateTime, nullable=True)

class ReactionTable(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    reaction_type = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    count = Column(Integer, nullable=False)

class ThreadTable(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    thread_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    owner_id = Column(Integer, nullable=False)
    admins = Column(ARRAY(Integer), nullable=False)
    members = Column(ARRAY(Integer), nullable=False)
    is_deleted = Column(Boolean, nullable=False)
    public_url = Column(String, nullable=True)
    is_public = Column(Boolean, nullable=True)

class ThreadMuteTable(Base):
    __tablename__ = "thread_mutes"
    
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    is_muted = Column(Boolean, nullable=False)
    
class ThreadMemberTable(Base):
    __tablename__ = "thread_members"
    
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    join_at = Column(DateTime, nullable=False)
    