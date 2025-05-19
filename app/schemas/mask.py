# app/schemas/mask.py
from pydantic import BaseModel

class MaskBase(BaseModel):
    name: str
    price: float

class MaskRead(MaskBase):
    id: int
    pharmacy_id: int
    class Config:
        orm_mode = True  # 讓 schema 能自動轉換 SQLAlchemy ORM 物件