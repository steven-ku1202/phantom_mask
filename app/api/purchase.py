# app/api/purchase.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.db.database import get_db
from app.db.models import User, Mask, Pharmacy, PurchaseHistory
from app.schemas.purchase import PurchaseCreate
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def purchase_mask(purchase: PurchaseCreate, db: AsyncSession = Depends(get_db)):
    # 查找使用者
    user = await db.get(User, purchase.user_id)
    if not user:
        raise HTTPException(404, detail="使用者不存在")

    # 查找口罩
    mask = await db.get(Mask, purchase.mask_id)
    if not mask:
        raise HTTPException(404, detail="口罩不存在")

    # 查找藥局
    pharmacy = await db.get(Pharmacy, purchase.pharmacy_id)
    if not pharmacy:
        raise HTTPException(404, detail="藥局不存在")

    price = mask.price

    # 檢查使用者餘額
    if user.cash_balance < price:
        raise HTTPException(400, detail="餘額不足")
    
    # 檢查藥局是否存在口罩庫存
    if mask.pharmacy_id != pharmacy.id:
        raise HTTPException(400, detail="該口罩不屬於指定藥局")

    # 扣除使用者金額
    user.cash_balance -= price
    user.cash_balance = round(user.cash_balance, 2)
    db.add(user)

    # 增加藥局金額
    pharmacy.cash_balance += price
    pharmacy.cash_balance = round(pharmacy.cash_balance, 2)
    db.add(pharmacy)

    # 建立交易紀錄
    now = datetime.now()
    record = PurchaseHistory(
        pharmacy=pharmacy.name,
        mask=mask.name,
        Amount=price,
        Date=now,
        user_id=user.id
    )
    db.add(record)

    # 寫入資料庫
    await db.commit()

    return {
        "message": "購買成功",
        "user": user.name,
        "mask": mask.name,
        "pharmacy": pharmacy.name,
        "Amount": price,
        "Date": now.strftime("%Y-%m-%d %H:%M:%S")
    }