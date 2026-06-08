from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from app.models.room import Room

class RoomService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_room(self, room_data: Dict[str, Any]) -> Room:
        room = Room(**room_data)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def get_rooms(self, skip: int = 0, limit: int = 100) -> List[Room]:
        return self.db.query(Room).filter(Room.is_active == True).offset(skip).limit(limit).all()
    
    def get_room(self, room_id: int) -> Optional[Room]:
        return self.db.query(Room).filter(Room.id == room_id).first()
    
    def update_room(self, room_id: int, update_data: Dict[str, Any]) -> Optional[Room]:
        room = self.get_room(room_id)
        if not room:
            return None
        
        for key, value in update_data.items():
            if hasattr(room, key):
                setattr(room, key, value)
        
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def delete_room(self, room_id: int) -> bool:
        room = self.get_room(room_id)
        if not room:
            return False
        
        # Soft delete - mark as inactive
        room.is_active = False
        self.db.commit()
        return True