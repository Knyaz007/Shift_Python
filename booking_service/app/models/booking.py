from sqlalchemy import Column, Integer, Date, ForeignKey, DateTime, func, Enum, String
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class BookingStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False)
    booking_date = Column(Date, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.ACTIVE)
    created_at = Column(DateTime, server_default=func.now())
    cancelled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(String(500))

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    time_slot = relationship("TimeSlot", back_populates="bookings")