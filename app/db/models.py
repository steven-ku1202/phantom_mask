from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

# 建立一個 Base 類別，作為所有資料表的基底。你後面定義的 Class table 就要繼承它。
Base = declarative_base()

class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    opening_hours = Column(JSONB, nullable=False)  # 儲存每週每日開店時間的 JSON 格式
    cash_balance = Column(Float, default=0.0)

    masks = relationship("Mask", back_populates="pharmacy")


class Mask(Base):
    __tablename__ = "masks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    pharmacy = relationship("Pharmacy", back_populates="masks")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cash_balance = Column(Float, default=0.0)

    purchaseHistories = relationship("PurchaseHistory", back_populates="user")


class PurchaseHistory(Base):
    __tablename__ = "purchaseHistories"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy = Column(String, nullable=False)
    mask = Column(String, nullable=False)
    Amount = Column(Float, default=0.0)
    Date = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="purchaseHistories")