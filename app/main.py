# app/main.py
from fastapi import FastAPI
from app.db.database import async_session, engine
from sqlalchemy.future import select
from sqlalchemy import text
from contextlib import asynccontextmanager
from app.db.models import Base, Pharmacy
from app.etl import loader

from app.api import pharmacies_open
from app.api import pharmacies_mask_sort 
from app.api import pharmacies_mask_filter
from app.api import users_transaction_top
from app.api import sales_summary
from app.api import relevance_search
from app.api import purchase

# 檢查資料表是否存在及初始化
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session() as session:
        # 先初始化資料表（不查詢前保證表存在）
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # 再查是否有資料
        result = await session.execute(select(Pharmacy))
        pharmacies = result.scalars().all()
        if not pharmacies:
            await loader.init_db()
            print("資料庫為空，初始資料未填寫")
            print("資料已導入")
        else:
            print("資料庫有資料，已初始化完成")
    yield


app = FastAPI(
    title="Pharmacy Mask API",
    description="支援藥局查詢、口罩銷售與購買管理的 API 伺服器",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "API is up and running!"}

# 掛載 router
app.include_router(pharmacies_open.router)
app.include_router(pharmacies_mask_sort.router)
app.include_router(pharmacies_mask_filter.router)
app.include_router(users_transaction_top.router)
app.include_router(sales_summary.router)
app.include_router(relevance_search.router)
app.include_router(purchase.router)