from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.schemas.room import RoomResponse
from app.services.room_service import RoomService
from app.services.slot_service import SlotService
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[RoomResponse])
async def get_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room_service = RoomService(db)
    return room_service.get_rooms(skip=skip, limit=limit)

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room_service = RoomService(db)
    room = room_service.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.get("/{room_id}/availability")
async def get_room_availability(
    room_id: int,
    booking_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    slot_service = SlotService(db)
    availability = slot_service.get_room_availability(room_id, booking_date)
    return availability