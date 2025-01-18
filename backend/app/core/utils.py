# app/core/utils.py
from datetime import datetime, timezone, timedelta


def get_utc_now() -> datetime:
    """Get current UTC time"""
    return datetime.now(timezone.utc)

def to_local_time(dt: datetime) -> datetime:
    """Convert UTC time to UTC+7"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt + timedelta(hours=7)  # Hardcode ke UTC+7