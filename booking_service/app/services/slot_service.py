from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, time
from typing import Optional, List, Dict, Any
from app.models.slot import TimeSlot
from app.models.booking import Booking, BookingStatus

class SlotService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_time_slot(self, slot_data: Dict[str, Any]) -> TimeSlot:
        slot = TimeSlot(**slot_data)
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot
    
    def get_room_slots(self, room_id: int) -> List[TimeSlot]:
        return self.db.query(TimeSlot).filter(TimeSlot.room_id == room_id).all()
    
    def is_slot_available(self, room_id: int, slot_id: int, booking_date: date) -> bool:
        # Check if slot exists for this room
        slot = self.db.query(TimeSlot).filter(
            TimeSlot.id == slot_id,
            TimeSlot.room_id == room_id
        ).first()
        
        if not slot:
            return False
        
        # Check for existing booking
        existing_booking = self.db.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.slot_id == slot_id,
            Booking.booking_date == booking_date,
            Booking.status == BookingStatus.ACTIVE
        ).first()
        
        return existing_booking is None
    
    def get_room_availability(self, room_id: int, booking_date: date) -> Dict[str, Any]:
        slots = self.get_room_slots(room_id)
        
        availability = []
        for slot in slots:
            is_available = self.is_slot_available(room_id, slot.id, booking_date)
            
            # Get booking info if not available
            booking_info = None
            if not is_available:
                booking = self.db.query(Booking).filter(
                    Booking.room_id == room_id,
                    Booking.slot_id == slot.id,
                    Booking.booking_date == booking_date,
                    Booking.status == BookingStatus.ACTIVE
                ).first()
                if booking:
                    booking_info = {
                        "booking_id": booking.id,
                        "user_id": booking.user_id
                    }
            
            availability.append({
                "slot_id": slot.id,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "slot_name": slot.slot_name,
                "is_available": is_available,
                "booking_info": booking_info
            })
        
        return {
            "room_id": room_id,
            "date": booking_date,
            "slots": availability
        }