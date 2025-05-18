# main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from db import get_db


app = FastAPI()


# 定義使用者資料格式（輸入的 JSON）
class UserCreate(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + PostgreSQL!"}


# ✅ 註冊 API：寫入資料庫
@app.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = models.User(username=user.username, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": f"User {new_user.username} registered successfully!"}


# ✅ 查詢 API：從資料庫抓出所有使用者
@app.get("/users")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users