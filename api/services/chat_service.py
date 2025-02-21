from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.chat import Message, Thread
from ..models.database_models import DBMessage, DBThread
from .mqtt_service import AsyncMQTTService
from .rabbitmq_service import AsyncRabbitMQService


class AsyncChatService:
    def __init__(self):
        self.mqtt = AsyncMQTTService()
        self.rabbitmq = AsyncRabbitMQService()
        
    async def initialize(self):
        await self.mqtt.connect()
        await self.rabbitmq.connect()
        
    async def cleanup(self):
        await self.mqtt.disconnect()
        await self.rabbitmq.close()
        
    async def send_message(self, message: Message, db: AsyncSession):
        # 创建数据库消息对象
        db_message = DBMessage(
            thread_id=message.thread_id,
            content=message.content,
            sender_id=message.sender_id
        )
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        
        # 异步发布到MQTT
        await self.mqtt.publish(
            f"thread/{message.thread_id}", 
            message.dict()
        )
        
        # 异步发送到RabbitMQ
        await self.rabbitmq.publish(
            'chat_messages',
            message.dict()
        )
        
        return message
    
    async def create_thread(self, thread: Thread, db: AsyncSession) -> Thread:
        # 创建数据库线程对象
        db_thread = DBThread(
            title=thread.title
        )
        db.add(db_thread)
        await db.commit()
        await db.refresh(db_thread)
        return thread
    
    async def get_thread_messages(
        self, 
        thread_id: int, 
        limit: int = 50,
        db: AsyncSession = None
    ) -> List[Message]:
        # 异步查询消息
        query = select(DBMessage).where(
            DBMessage.thread_id == thread_id
        ).limit(limit)
        result = await db.execute(query)
        messages = result.scalars().all()
        return [
            Message(
                id=msg.id,
                thread_id=msg.thread_id,
                content=msg.content,
                sender_id=msg.sender_id,
                created_at=msg.created_at
            ) for msg in messages
        ] 