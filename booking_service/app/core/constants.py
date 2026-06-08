from enum import Enum

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"

# Predefined time slots (you can customize these)
TIME_SLOTS = [
    {"id": 1, "start": "09:00", "end": "11:00", "name": "Morning Slot"},
    {"id": 2, "start": "11:00", "end": "13:00", "name": "Late Morning Slot"},
    {"id": 3, "start": "13:00", "end": "15:00", "name": "Afternoon Slot"},
    {"id": 4, "start": "15:00", "end": "17:00", "name": "Late Afternoon Slot"},
    {"id": 5, "start": "17:00", "end": "19:00", "name": "Evening Slot"},
]