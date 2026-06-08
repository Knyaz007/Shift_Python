from pydantic import BaseModel
from datetime import time
from typing import Optional

class TimeSlotCreate(BaseModel):
    room_id: int
    start_time: time
    end_time: time
    slot_name: Optional[str] = None

class TimeSlotResponse(BaseModel):
    id: int
    room_id: int
    start_time: time
    end_time: time
    slot_name: Optional[str]

    class Config:
        from_attributes = True