from .mqtt_service import AsyncMQTTService
from .rabbitmq_service import AsyncRabbitMQService
from ..models.chat import Message, Thread
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

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
        # 异步保存到数据库
        # db.add(message)
        # await db.commit()
        # await db.refresh(message)
        
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
        # 异步创建线程
        # db.add(thread)
        # await db.commit()
        # await db.refresh(thread)
        return thread
    
    async def get_thread_messages(
        self, 
        thread_id: int, 
        limit: int = 50,
        db: AsyncSession = None
    ) -> List[Message]:
        # 异步查询消息
        # query = select(Message).where(Message.thread_id == thread_id)
        # result = await db.execute(query)
        # messages = result.scalars().all()
        return [] 