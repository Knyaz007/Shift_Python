from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.booking import BookingStatus

class BookingCreate(BaseModel):
    room_id: int
    slot_id: int
    booking_date: date

class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    slot_id: int
    booking_date: date
    status: BookingStatus
    created_at: datetime
    cancelled_at: Optional[datetime]
    cancellation_reason: Optional[str]
    
    # Additional info
    room_name: Optional[str] = None
    user_name: Optional[str] = None
    slot_time: Optional[str] = None

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    cancellation_reason: Optional[str] = None