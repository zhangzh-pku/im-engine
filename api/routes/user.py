from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import settings
from api.core.database import get_db
from api.models.base import FriendRequestTable, FriendTable, UserTable
from api.models.users import LoginRequest, RegisterRequest
from api.utils import get_current_user_id

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.name == request.name))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="未找到用户")
    def verify_password(password: str):
        hashed_password = user.hashed_password
        return pwd_context.verify(password, hashed_password)
    if not verify_password(request.password):
        raise HTTPException(status_code=401, detail="密码错误")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = jwt.encode(
        {"sub": user.id, "exp": datetime.now().timestamp() + access_token_expires},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {"access_token": token_data, "token_type": "Bearer"}

@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.name == request.name))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="用户已存在")
    hashed_password = pwd_context.hash(request.password)
    user = UserTable(name=request.name, hashed_password=hashed_password, create_at=datetime.now())
    db.add(user)
    friend = FriendTable(user_id=user.id, friend_ids=[])
    db.add(friend)
    friend_request = FriendRequestTable(user_id=user.id, friends_status={})
    db.add(friend_request)
    await db.flush()
    return {"message": "注册成功", "id": user.id}

@router.post("friends/{friend_id}")
async def accept_friend(friend_id: int,id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.id.in_([id, friend_id])))
    users = result.scalars().all()
    if len(users) != 2:
        raise HTTPException(status_code=404, detail="用户不存在")
    friends = await db.execute(select(FriendTable).where(FriendTable.user_id.in_([id, friend_id])))
    friends_dict = {f.user_id: f.friend_ids for f in friends.scalars().all()}
    if id not in friends_dict:
        friend1 = FriendTable(user_id=id, friend_ids=[friend_id])
        db.add(friend1)
    else:
        friend1 = friends_dict[id]
        if friend_id not in friend1.friend_ids:
            friend1.friend_ids.append(friend_id)
    if friend_id not in friends_dict:
        friend2 = FriendTable(user_id=friend_id, friend_ids=[id])
        db.add(friend2)
    else:
        friend2 = friends_dict[friend_id]
        if id not in friend2.friend_ids:
            friend2.friend_ids.append(id)
    friend_request = await db.execute(select(FriendRequestTable).where(FriendRequestTable.user_id == friend_id, FriendRequestTable.friend_id == id))
    friend_request = friend_request.scalar_one_or_none()
    if friend_request:
        friend_request.status = 1
    return {"message": "添加好友成功"}

@router.post("/friends/requests/{friend_id}/reject")
async def reject_friend_request(friend_id: int, id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    friend_request = await db.execute(select(FriendRequestTable).where(FriendRequestTable.user_id == id, FriendRequestTable.friend_id == friend_id))
    friend_request = friend_request.scalar_one_or_none()
    if friend_request:
        friend_request.status = 2
    else:
        raise HTTPException(status_code=404, detail="好友请求不存在")
    return {"message": "拒绝好友请求成功"}
    
@router.post("/friends/requests/{friend_id}")
async def send_friend_request(friend_id: int, id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    friend_request = FriendRequestTable(user_id=id, friend_id=friend_id, status=0)
    db.add(friend_request)
    return {"message": "发送好友请求成功"}
    
@router.get("/friends/requests")
async def get_friend_requests(id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FriendRequestTable).where(FriendRequestTable.user_id == id))
    friend_requests = result.scalars().all()
    return {"friend_requests": friend_requests}

@router.delete("/friends/{friend_id}")
async def delete_friend(friend_id: int, id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FriendTable).where(FriendTable.user_id.in_([id, friend_id])))
    friends_dict = {f.user_id: f.friend_ids for f in result.scalars().all()}
    if id not in friends_dict or friend_id not in friends_dict:
        logger.warning(f"用户{id}不存在好友{friend_id}")
    if id in friends_dict[friend_id]:
        friends_dict[friend_id].remove(id)
    if friend_id in friends_dict[id]:
        friends_dict[id].remove(friend_id)
    return {"message": "删除好友成功"}