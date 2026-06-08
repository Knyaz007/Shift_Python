import pytest
from datetime import date, timedelta
from app.services.booking_service import BookingService
from app.services.room_service import RoomService
from app.services.slot_service import SlotService
from app.models.room import Room
from app.models.slot import TimeSlot

@pytest.fixture
def test_room(db):
    room = Room(
        name="Test Room",
        capacity=10,
        location="Test Location"
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@pytest.fixture
def test_slot(db, test_room):
    slot = TimeSlot(
        room_id=test_room.id,
        start_time="09:00",
        end_time="11:00",
        slot_name="Morning Slot"
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

def test_create_booking(db, test_user, test_room, test_slot):
    booking_service = BookingService(db)
    booking_date = date.today() + timedelta(days=1)
    
    booking = booking_service.create_booking(
        user_id=test_user.id,
        room_id=test_room.id,
        slot_id=test_slot.id,
        booking_date=booking_date
    )
    
    assert booking is not None
    assert booking.user_id == test_user.id
    assert booking.room_id == test_room.id

def test_create_duplicate_booking(db, test_user, test_room, test_slot):
    booking_service = BookingService(db)
    booking_date = date.today() + timedelta(days=1)
    
    # First booking should succeed
    booking_service.create_booking(test_user.id, test_room.id, test_slot.id, booking_date)
    
    # Second booking should fail
    with pytest.raises(ValueError, match="This time slot is already booked"):
        booking_service.create_booking(test_user.id, test_room.id, test_slot.id, booking_date)

def test_cancel_booking(db, test_user, test_room, test_slot):
    booking_service = BookingService(db)
    booking_date = date.today() + timedelta(days=1)
    
    booking = booking_service.create_booking(
        test_user.id, test_room.id, test_slot.id, booking_date
    )
    
    cancelled = booking_service.cancel_booking(booking.id, test_user.id, "employee")
    assert cancelled.status == "cancelled"