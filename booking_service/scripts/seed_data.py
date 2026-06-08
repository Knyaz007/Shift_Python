#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.room import Room
from app.models.slot import TimeSlot
from app.models.user import User
from app.core.security import hash_password
from app.core.constants import UserRole
from datetime import time

def seed_database():
    print(f"Connecting to database: {settings.DATABASE_URL}")
    
    engine = create_engine(settings.DATABASE_URL)
    
    # Создаем все таблицы
    Base.metadata.drop_all(bind=engine)  # Очищаем старые таблицы
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role=UserRole.ADMIN,
            full_name="System Administrator"
        )
        db.add(admin)
        
        # Create regular user
        user = User(
            username="user",
            email="user@example.com",
            hashed_password=hash_password("user123"),
            role=UserRole.EMPLOYEE,
            full_name="Regular User"
        )
        db.add(user)
        
        # Create rooms
        rooms_data = [
            {"name": "Conference Room A", "capacity": 10, "location": "Floor 1", 
             "description": "Large conference room with projector", "equipment": "Projector, Whiteboard, Video Conferencing"},
            {"name": "Meeting Room B", "capacity": 6, "location": "Floor 2", 
             "description": "Small meeting room", "equipment": "Whiteboard, TV Screen"},
            {"name": "Board Room", "capacity": 20, "location": "Floor 3", 
             "description": "Executive board room", "equipment": "Projector, Sound System, Video Conferencing, Whiteboard"},
            {"name": "Creative Space", "capacity": 8, "location": "Floor 1", 
             "description": "Creative brainstorming space", "equipment": "Whiteboard, Sticky Notes, TV Screen"},
        ]
        
        rooms = []
        for room_data in rooms_data:
            room = Room(**room_data)
            db.add(room)
            rooms.append(room)
        
        db.commit()
        
        # Create time slots for each room
        time_slots_config = [
            {"start": "09:00", "end": "11:00", "name": "Morning Slot"},
            {"start": "11:00", "end": "13:00", "name": "Late Morning Slot"},
            {"start": "13:00", "end": "15:00", "name": "Afternoon Slot"},
            {"start": "15:00", "end": "17:00", "name": "Late Afternoon Slot"},
            {"start": "17:00", "end": "19:00", "name": "Evening Slot"},
        ]
        
        for room in rooms:
            for slot_config in time_slots_config:
                slot = TimeSlot(
                    room_id=room.id,
                    start_time=time.fromisoformat(slot_config["start"]),
                    end_time=time.fromisoformat(slot_config["end"]),
                    slot_name=slot_config["name"]
                )
                db.add(slot)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print(f"👤 Created admin user: admin/admin123")
        print(f"👤 Created regular user: user/user123")
        print(f"🏢 Created {len(rooms)} rooms with {len(time_slots_config)} time slots each")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()