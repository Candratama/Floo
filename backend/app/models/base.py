from datetime import datetime
from sqlmodel import SQLModel, Field
from app.core.utils import get_utc_now

class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)