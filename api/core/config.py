from pydantic_settings import BaseSettings
import os
import dotenv

dotenv.load_dotenv()

class Settings(BaseSettings):
    # FastAPI设置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "IM engine via python"
    
    # MQTT设置
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST")
    MQTT_BROKER_PORT: int = os.getenv("MQTT_BROKER_PORT")
    MQTT_TOPIC_PREFIX: str = "chat"
    MQTT_BROKER_USERNAME: str = os.getenv("MQTT_BROKER_USERNAME")
    MQTT_BROKER_PASSWORD: str = os.getenv("MQTT_BROKER_PASSWORD")
    # RabbitMQ设置
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT: int = os.getenv("RABBITMQ_PORT")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD")
    
    # 数据库设置
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # JWT设置
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    class Config:
        case_sensitive = True

settings = Settings() 