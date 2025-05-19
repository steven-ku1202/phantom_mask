# app/api/pharmacies_open.py
from fastapi import APIRouter, Depends, Query
from enum import Enum
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models import Pharmacy
from datetime import datetime  #, time as dt_time
import pytz
from app.func.is_open import is_open

class HourEnum(str, Enum):
    h00 = "00"
    h01 = "01"
    h02 = "02"
    h03 = "03"
    h04 = "04"
    h05 = "05"
    h06 = "06"
    h07 = "07"
    h08 = "08"
    h09 = "09"
    h10 = "10"
    h11 = "11"
    h12 = "12"
    h13 = "13"
    h14 = "14"
    h15 = "15"
    h16 = "16"
    h17 = "17"
    h18 = "18"
    h19 = "19"
    h20 = "20"
    h21 = "21"
    h22 = "22"
    h23 = "23"

class MinuteEnum(str, Enum):
    m00 = "00"
    m10 = "10"
    m20 = "20"
    m30 = "30"
    m40 = "40"
    m50 = "50"

class WeekdayEnum(str, Enum):
    Monday = "Mon"
    Tuesday = "Tue"
    Wednesday = "Wed"
    Thursday = "Thur"
    Friday = "Fri"
    Saturday = "Sat"
    Sunday = "Sun"


router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

@router.get("/open")
async def get_open_pharmacies( 
    hour: Optional[HourEnum] = Query(default=None, description="查詢小時(若未指定，則取當前系統小時)"),
    minute: Optional[MinuteEnum] = Query(default=None, description="查詢分鐘(若未指定，則取當前系統分鐘)"),
    weekday: Optional[WeekdayEnum] = Query(default=None, description="查詢星期(若未指定，則取當前系統星期)"),
    db: AsyncSession = Depends(get_db)):
    
    # 從資料庫取得所有 Pharmacy 藥局模型的資料列，並轉為 Python list。
    query = select(Pharmacy)
    result = await db.execute(query)
    pharmacies = result.scalars().all()


    # 若未指定 time，則取當前系統時間
    if hour is None:
        now = datetime.now(pytz.timezone("Asia/Taipei"))
        hour = now.replace(second=0, microsecond=0).time().strftime("%H")
    if minute is None:
        now = datetime.now(pytz.timezone("Asia/Taipei"))
        minute = now.replace(second=0, microsecond=0).time().strftime("%M")
    time = hour + ":" + minute

    # 若未指定 weekday，則取當前系統時間
    if weekday is None:
        now = datetime.now(pytz.timezone("Asia/Taipei"))
        weekday = now.strftime("%a")  # 轉成 Mon, Tue 等格式

    open_pharmacies = []

    for pharmacy in pharmacies:
        hours = pharmacy.opening_hours
        if is_open(pharmacy.opening_hours, weekday, time):
            open_pharmacies.append(pharmacy.name)

    return {"time":time, "weekday":weekday, "open_pharmacies": open_pharmacies}