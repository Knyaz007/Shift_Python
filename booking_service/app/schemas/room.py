from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    name: str
    capacity: int
    location: Optional[str] = None
    description: Optional[str] = None
    equipment: Optional[str] = None

class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    location: Optional[str]
    description: Optional[str]
    is_active: bool
    equipment: Optional[str]

    class Config:
        from_attributes = True

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    equipment: Optional[str] = None