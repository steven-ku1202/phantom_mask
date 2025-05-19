# app/api/relevance_search.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, literal_column
from app.db.database import get_db
from app.db.models import Pharmacy, Mask

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def relevance_search(
    keyword: str = Query(..., min_length=1),
    target: str = Query(default="all", enum=["pharmacy", "mask", "all"], description="搜尋對象"),
    limit: int = Query(default=10, description="搜尋資料筆數"),
    db: AsyncSession = Depends(get_db)
):
    results = []

    if target in ["mask", "all"]:
        stmt = (
            select(
                Mask.id,
                Mask.name,
                func.similarity(Mask.name, keyword).label("relevance"),
                literal_column("'mask'").label("type")
            )
            .where(func.similarity(Mask.name, keyword) > 0.1)
            .order_by(desc("relevance"))
            .limit(limit)
        )
        result = await db.execute(stmt)
        results.extend(result.all())

    if target in ["pharmacy", "all"]:
        stmt = (
            select(
                Pharmacy.id,
                Pharmacy.name,
                func.similarity(Pharmacy.name, keyword).label("relevance"),
                literal_column("'pharmacy'").label("type")
            )
            .where(func.similarity(Pharmacy.name, keyword) > 0.1)
            .order_by(desc("relevance"))
            .limit(limit)
        )
        result = await db.execute(stmt)
        results.extend(result.all())

    # 統一排序 relevance（若 mask + pharmacy 一起搜）
    results.sort(key=lambda x: x.relevance, reverse=True)

    return [
        {
            "type": r.type,
            "id": r.id,
            "name": r.name,
            "relevance": round(r.relevance, 4)
        }
        for r in results
    ]