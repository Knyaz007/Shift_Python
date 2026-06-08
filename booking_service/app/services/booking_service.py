from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from app.models.booking import Booking, BookingStatus
from app.models.room import Room
from app.models.user import User
from app.models.slot import TimeSlot
from app.services.slot_service import SlotService

class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.slot_service = SlotService(db)
    
    def create_booking(self, user_id: int, room_id: int, slot_id: int, booking_date: date) -> Booking:
        # Check if slot exists
        slot = self.db.query(TimeSlot).filter(TimeSlot.id == slot_id, TimeSlot.room_id == room_id).first()
        if not slot:
            raise ValueError("Invalid time slot for this room")
        
        # Check if slot is available
        if not self.slot_service.is_slot_available(room_id, slot_id, booking_date):
            raise ValueError("This time slot is already booked")
        
        # Check if booking date is not in the past
        if booking_date < date.today():
            raise ValueError("Cannot book for past dates")
        
        # Create booking
        booking = Booking(
            user_id=user_id,
            room_id=room_id,
            slot_id=slot_id,
            booking_date=booking_date,
            status=BookingStatus.ACTIVE
        )
        
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking
    
    def get_booking(self, booking_id: int) -> Optional[Booking]:
        return self.db.query(Booking).filter(Booking.id == booking_id).first()
    
    def get_user_bookings(self, user_id: int, skip: int = 0, limit: int = 100, status: Optional[str] = None):
        query = self.db.query(Booking).filter(Booking.user_id == user_id)
        
        if status:
            query = query.filter(Booking.status == status)
        
        bookings = query.offset(skip).limit(limit).all()
        
        # Enrich with additional data
        for booking in bookings:
            room = self.db.query(Room).filter(Room.id == booking.room_id).first()
            slot = self.db.query(TimeSlot).filter(TimeSlot.id == booking.slot_id).first()
            booking.room_name = room.name if room else None
            booking.slot_time = f"{slot.start_time}-{slot.end_time}" if slot else None
        
        return bookings
    
    def cancel_booking(self, booking_id: int, user_id: int, user_role: str, reason: Optional[str] = None) -> Booking:
        booking = self.get_booking(booking_id)
        
        if not booking:
            raise ValueError("Booking not found")
        
        # Check permissions
        if booking.user_id != user_id and user_role != "admin":
            raise PermissionError("You don't have permission to cancel this booking")
        
        # Check if booking date is in the past
        if booking.booking_date < date.today():
            raise ValueError("Cannot cancel past bookings")
        
        # Update booking
        booking.status = BookingStatus.CANCELLED
        booking.cancelled_at = datetime.now()
        booking.cancellation_reason = reason
        
        self.db.commit()
        self.db.refresh(booking)
        return booking
    
    def get_all_bookings(self, skip: int = 0, limit: int = 100, user_id: Optional[int] = None, 
                        room_id: Optional[int] = None, date_filter: Optional[date] = None) -> List[Booking]:
        query = self.db.query(Booking)
        
        if user_id:
            query = query.filter(Booking.user_id == user_id)
        if room_id:
            query = query.filter(Booking.room_id == room_id)
        if date_filter:
            query = query.filter(Booking.booking_date == date_filter)
        
        bookings = query.offset(skip).limit(limit).all()
        
        # Enrich with additional data
        for booking in bookings:
            room = self.db.query(Room).filter(Room.id == booking.room_id).first()
            user = self.db.query(User).filter(User.id == booking.user_id).first()
            slot = self.db.query(TimeSlot).filter(TimeSlot.id == booking.slot_id).first()
            booking.room_name = room.name if room else None
            booking.user_name = user.username if user else None
            booking.slot_time = f"{slot.start_time}-{slot.end_time}" if slot else None
        
        return bookings