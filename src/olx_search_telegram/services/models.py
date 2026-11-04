from datetime import datetime
from pydantic import BaseModel


class ScheduleJob(BaseModel):
    id: int | None
    url: str
    interval_minutes: int
    is_active: bool
    last_run_at: datetime | None
