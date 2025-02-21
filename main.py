from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.core.config import settings
from api.routes import chat
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # # 启动时执行
    # await chat.chat_service.initialize()
    # yield
    # # 关闭时执行
    # await chat.chat_service.cleanup()
    pass
    
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# 注册路由
app.include_router(chat.router, prefix=settings.API_V1_STR + "/chat")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 