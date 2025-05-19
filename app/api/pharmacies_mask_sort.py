# app/api/pharmacies_mask.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from app.db.database import get_db
from app.db.models import Pharmacy, Mask
from app.schemas.mask import MaskBase

router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

@router.get("/masks")
async def get_pharmacy_masks_sort(
    pharmacy_id: int = Query(..., description="藥局id (ex:1)"),
    sort_by: str = Query(default="name", enum=["name", "price"], description="依（名稱、價格）排序"),
    order: str = Query(default="ascending", enum=["ascending", "descending"], description="升冪或降冪"),
    db: AsyncSession = Depends(get_db)):
    
    # 檢查藥局是否存在
    pharmacy = await db.get(Pharmacy, pharmacy_id)
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    # 設定排序
    sort_column = Mask.name if sort_by == "name" else Mask.price
    sort_order = asc if order == "ascending" else desc

    stmt = select(Mask).where(Mask.pharmacy_id == pharmacy_id).order_by(sort_order(sort_column))
    result = await db.execute(stmt)
    masks = result.scalars().all()

    return {"pharmacy_id":pharmacy.id, "pharmacy_name":pharmacy.name, "sort_by":sort_by, "order":order, "masks":[{"name": m.name, "price": m.price} for m in masks]}