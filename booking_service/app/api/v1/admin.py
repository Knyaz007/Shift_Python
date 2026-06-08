from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.booking import BookingResponse
from app.services.room_service import RoomService
from app.services.booking_service import BookingService
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.db import get_db
from app.models.user import User

router = APIRouter(dependencies=[Depends(require_admin)])

# Room management
@router.post("/rooms", response_model=RoomResponse)
async def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room_service = RoomService(db)
    return room_service.create_room(room_data.dict())

@router.put("/rooms/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int,
    room_data: RoomUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room_service = RoomService(db)
    room = room_service.update_room(room_id, room_data.dict(exclude_unset=True))
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/rooms/{room_id}")
async def delete_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room_service = RoomService(db)
    if room_service.delete_room(room_id):
        return {"message": "Room deleted successfully"}
    raise HTTPException(status_code=404, detail="Room not found")

# User management
@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    return auth_service.get_users(skip, limit)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    user = auth_service.update_user(user_id, user_data.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    if auth_service.delete_user(user_id):
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Admin booking management
@router.get("/bookings", response_model=List[BookingResponse])
async def get_all_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[int] = None,
    room_id: Optional[int] = None,
    date_filter: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking_service = BookingService(db)
    return booking_service.get_all_bookings(skip, limit, user_id, room_id, date_filter)

@router.post("/bookings/{booking_id}/cancel")
async def admin_cancel_booking(
    booking_id: int,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking_service = BookingService(db)
    try:
        booking = booking_service.cancel_booking(booking_id, current_user.id, "admin", reason)
        return {"message": "Booking cancelled successfully by admin"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))