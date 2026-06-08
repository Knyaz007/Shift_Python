from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String(200))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    equipment = Column(String(500))  # Comma-separated equipment list

    bookings = relationship("Booking", back_populates="room", cascade="all, delete-orphan")
    slots = relationship("TimeSlot", back_populates="room", cascade="all, delete-orphan")