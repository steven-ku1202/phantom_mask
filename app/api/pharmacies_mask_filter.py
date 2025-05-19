# app/api/pharmacies_mask_filter.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from app.db.database import get_db
from app.db.models import Pharmacy, Mask

router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

@router.get("/filter-mask-price")
async def filter_pharmacies_by_mask_count(
    min_price: float = Query(..., ge=0, description="設定價格下限"),
    max_price: float = Query(..., gt=0, description="設定價格上限"),
    threshold: int = Query(..., description="設定口罩數量的門檻"),
    comparison: str = Query(..., enum=["more", "fewer"]),
    db: AsyncSession = Depends(get_db)):

    # 聚合：每間藥局的 mask 數量（僅限價格在範圍內）
    stmt = (
        select(
            Pharmacy.id,
            Pharmacy.name,
            func.count(Mask.id).label("mask_count")
        )
        .join(Mask, Pharmacy.id == Mask.pharmacy_id)
        .where(Mask.price.between(min_price, max_price))
        .group_by(Pharmacy.id)
    )

    result = await db.execute(stmt)
    rows = result.all()

    # 過濾 mask 數量（手動比對）
    if comparison == "more":
        filtered = [dict(id=row.id, name=row.name, mask_count=row.mask_count) for row in rows if row.mask_count >= threshold]
    else:
        filtered = [dict(id=row.id, name=row.name, mask_count=row.mask_count) for row in rows if row.mask_count <= threshold]

    return filtered