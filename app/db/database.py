# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 建立一個「非同步」的資料庫引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 建立「非同步 session 工廠」
# 需要操作資料表（例如新增一筆使用者），就會從這個 async_session 產生 session 物件，並透過 session 對資料庫下指令。
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session