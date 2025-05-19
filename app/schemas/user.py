# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    cash_balance: Optional[float] = 0.0

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True  # 讓 schema 能自動轉換 SQLAlchemy ORM 物件