import re
from datetime import datetime, time

def is_open(opening_hours_str: str, weekday: str, time: str) -> bool:
    time = datetime.strptime(time, "%H:%M").time()

    # 分段處理（例如 "Mon - Fri 08:00 - 17:00 / Sat 10:00 - 14:00"）
    parts = [part.strip() for part in opening_hours_str.split("/")]

    for part in parts:
        # 用正則擷取日期段與時間段
        match = re.match(r"([A-Za-z,\s\-]+)\s+(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})", part)
        if not match:
            continue

        day_part, start_str, end_str = match.groups()
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()

        # 把 day_part 轉成 set，例如 "Mon - Fri" → {"Mon", "Tue", ..., "Fri"}
        days_set = set()
        weekday_list = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
        for segment in day_part.split(","):
            segment = segment.strip()
            if "-" in segment:
                start_day, end_day = map(str.strip, segment.split("-"))
                start_idx = weekday_list.index(start_day)
                end_idx = weekday_list.index(end_day)
                if start_idx <= end_idx:
                    days_set.update(weekday_list[start_idx:end_idx + 1])
            else:
                days_set.add(segment)

         # 判斷今天是否在其中，且時間介於範圍內
        if weekday in days_set: 
            if start_time < end_time:
                return start_time <= time <= end_time
            else:  # 開到半夜
                return ~(end_time <= time <= start_time)

        
    return False