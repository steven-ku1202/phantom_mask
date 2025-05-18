import os
import json
import asyncio
from db.database import engine, async_session
from db.models import Base, Pharmacy, Mask, User, PurchaseHistory
from datetime import datetime

# 獲得專案根目錄的絕對路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH_pharmacies = os.path.join(BASE_DIR, "data", "pharmacies.json")
DATA_PATH_users = os.path.join(BASE_DIR, "data", "users.json")

async def init_db():
    # 建立資料表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)   # 如果'表'不存在，就會建立；如果已存在，不會重建

    # 載入 pharmacies JSON
    with open(DATA_PATH_pharmacies, "r", encoding="utf-8") as f:
        pharmacies_data = json.load(f)

    # 寫入資料
    async with async_session() as session:
        for p in pharmacies_data:
            pharmacy = Pharmacy(
                name=p["name"],
                cash_balance=p["cashBalance"],
                opening_hours=p["openingHours"]
            )
            for m in p["masks"]:
                mask = Mask(name=m["name"], price=m["price"])
                pharmacy.masks.append(mask)
            session.add(pharmacy)
        await session.commit()

    
    # 載入 users JSON
    with open(DATA_PATH_users, "r", encoding="utf-8") as f:
        users_data = json.load(f)

    # 寫入資料
    async with async_session() as session:
        for p in users_data:
            user = User(
                name=p["name"],
                cash_balance=p["cashBalance"]
            )
            for m in p["purchaseHistories"]:
                dt = datetime.strptime(m["transactionDate"], "%Y-%m-%d %H:%M:%S")  # 字串轉 datetime
                purchaseHistory = PurchaseHistory(pharmacy=m["pharmacyName"], mask=m["maskName"], Amount=m["transactionAmount"], Date=dt)
                user.purchaseHistories.append(purchaseHistory)
            session.add(user)
        await session.commit()
        

if __name__ == "__main__":
    asyncio.run(init_db())