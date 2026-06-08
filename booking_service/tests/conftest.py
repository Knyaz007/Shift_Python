import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.base import Base
from app.models.user import User
from app.models.room import Room
from app.models.booking import Booking
from app.models.slot import TimeSlot
from app.core.security import hash_password
from app.core.constants import UserRole

# Используем PostgreSQL из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@test-db:5432/test_booking_db")

# Создаем engine для PostgreSQL
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Создает таблицы перед тестами и удаляет после"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    """Фикстура сессии БД"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Откатываем изменения после каждого теста
        db.close()

@pytest.fixture
def client(db):
    """Тестовый клиент"""
    return TestClient(app)

@pytest.fixture
def test_user(db):
    """Создает тестового пользователя"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpass"),
        role=UserRole.EMPLOYEE,
        full_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_admin(db):
    """Создает тестового администратора"""
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("adminpass"),
        role=UserRole.ADMIN,
        full_name="Admin User"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture
def test_room(db):
    """Создает тестовую комнату"""
    from app.models.room import Room
    room = Room(
        name="Conference Room",
        capacity=10,
        description="Test room"
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@pytest.fixture
def auth_client(client, test_user):
    """Клиент с авторизацией"""
    # Получаем токен
    response = client.post("/api/v1/auth/login", json={
        "username": test_user.username,
        "password": "testpass"
    })
    token = response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client