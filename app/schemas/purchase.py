# app/schemas/pharmacy.py
from pydantic import BaseModel
from datetime import datetime


class PurchaseBase(BaseModel):
    pharmacy_id: int
    mask_id: int
    Date: datetime

class PurchaseCreate(PurchaseBase):
    user_id: int
    class Config:
        orm_mode = True  # 讓 schema 能自動轉換 SQLAlchemy ORM 物件