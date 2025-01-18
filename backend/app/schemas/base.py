from pydantic import BaseModel
from datetime import datetime
from app.core.utils import to_local_time

class TimestampResponseMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: to_local_time(dt).isoformat()
        }