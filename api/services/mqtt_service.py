import asyncio
import json
import uuid
from typing import Callable, Dict

from gmqtt import Client as MQTTClient

from ..core.config import settings


class AsyncMQTTService:
    def __init__(self):
        # 使用随机客户端ID避免冲突
        client_id = f'mqtt-client-{str(uuid.uuid4())}'
        self.client = MQTTClient(client_id)
        self.message_handlers: Dict[str, Callable] = {}
        
        # 设置回调
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    async def connect(self):
        await self.client.connect(
            settings.MQTT_BROKER_HOST,
            settings.MQTT_BROKER_PORT,
            username=settings.MQTT_BROKER_USERNAME,
            password=settings.MQTT_BROKER_PASSWORD
        )

    async def disconnect(self):
        await self.client.disconnect()

    def on_connect(self, client, flags, rc, properties):
        print(f"Connected to MQTT broker with result code: {rc}")

    def on_disconnect(self, client, packet, exc=None):
        print("Disconnected from MQTT broker")

    def on_message(self, client, topic, payload, qos, properties):
        try:
            message = json.loads(payload.decode())
            if topic in self.message_handlers:
                asyncio.create_task(self.message_handlers[topic](message))
        except Exception as e:
            print(f"Error processing message: {e}")

    async def publish(self, topic: str, message: dict, qos: int = 1):
        full_topic = f"{settings.MQTT_TOPIC_PREFIX}/{topic}"
        await self.client.publish(
            full_topic, 
            json.dumps(message).encode(),
            qos=qos
        )

    async def subscribe(self, topic: str, handler: Callable):
        full_topic = f"{settings.MQTT_TOPIC_PREFIX}/{topic}"
        self.message_handlers[full_topic] = handler
        await self.client.subscribe([(full_topic, 1)]) 