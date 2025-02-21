from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class DBThread(Base):
    __tablename__ = "threads"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("DBMessage", back_populates="thread")

class DBMessage(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    content = Column(Text)
    sender_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    thread = relationship("DBThread", back_populates="messages") 