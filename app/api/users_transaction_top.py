# app/api/users_transaction_top.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.db.database import get_db
from app.db.models import PurchaseHistory, User
from datetime import datetime, timedelta

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/top-users-by-transaction-amount")
async def get_top_users_by_transaction_count(
    start_date: str = Query(default=None, description="起始日期, 格式: YYYY-MM-DD"),
    end_date: str = Query(default=None, description="結束日期, 格式: YYYY-MM-DD"),
    top_n: int = Query(default=5, gt=0, description="名次設定 (預設:5)"),
    db: AsyncSession = Depends(get_db)
):
    
    # 轉換日期字串
    if start_date is None:
        start_date = "1900-01-01"
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format, should be YYYY-MM-DD"}

    if end_date is None:
        end_date = "2100-01-01"
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
    else:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
        except ValueError:
            return {"error": "Invalid date format, should be YYYY-MM-DD"}

    stmt = (
        select(
            User.id,
            User.name,
            func.count(PurchaseHistory.id).label("transaction_count")
        )
        .join(PurchaseHistory, PurchaseHistory.user_id == User.id)
        .where(PurchaseHistory.Date.between(start, end))
        .group_by(User.id)
        .order_by(desc("transaction_count"))
        .limit(top_n)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "user_id": row.id,
            "name": row.name,
            "transaction_count": row.transaction_count
        }
        for row in rows
    ]