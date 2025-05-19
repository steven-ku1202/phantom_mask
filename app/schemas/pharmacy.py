# app/schemas/pharmacy.py
from pydantic import BaseModel
from typing import Optional


class PharmacyBase(BaseModel):
    name: str
    opening_hours: str
    cash_balance: Optional[float] = 0.0

class PharmacyRead(PharmacyBase):
    id: int
    class Config:
        orm_mode = True  # 讓 schema 能自動轉換 SQLAlchemy ORM 物件