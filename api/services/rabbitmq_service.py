import aio_pika
from ..core.config import settings
import json
from typing import Callable

class AsyncRabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._queues = {}

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD
        )
        self.channel = await self.connection.channel()
        
        # 声明队列
        self._queues['chat_messages'] = await self.channel.declare_queue(
            'chat_messages',
            durable=True
        )
        self._queues['notifications'] = await self.channel.declare_queue(
            'notifications',
            durable=True
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def publish(self, queue: str, message: dict):
        if not self.channel:
            raise RuntimeError("RabbitMQ connection not established")
            
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue
        )

    async def consume(self, queue: str, callback: Callable):
        if queue not in self._queues:
            raise ValueError(f"Queue {queue} not declared")
            
        async def _callback(message: aio_pika.IncomingMessage):
            async with message.process():
                data = json.loads(message.body.decode())
                await callback(data)

        await self._queues[queue].consume(_callback) 