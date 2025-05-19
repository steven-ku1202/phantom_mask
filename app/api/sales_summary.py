# app/api/sales_summary.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.db.models import PurchaseHistory
from datetime import datetime, timedelta

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/sales-summary")
async def get_sales_summary(
    start_date: str = Query(default=None, description="起始日期, 格式: YYYY-MM-DD"),
    end_date: str = Query(default=None, description="結束日期, 格式: YYYY-MM-DD"),
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
            func.count(PurchaseHistory.id).label("total_transactions"),
            func.sum(PurchaseHistory.Amount).label("total_value")
        )
        .where(PurchaseHistory.Date.between(start, end))
    )

    result = await db.execute(stmt)
    total_transactions, total_value = result.one()

    return {
        "total_mask_sales": total_transactions,  # 若每筆只對應一項商品
        "total_transaction_value": round(float(total_value or 0.0), 2)
    }