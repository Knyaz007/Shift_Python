import pytest
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.constants import UserRole

def test_register_user(db):
    auth_service = AuthService(db)
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "full_name": "New User"
    }
    
    user = auth_service.register_user(user_data)
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.role == UserRole.EMPLOYEE

def test_register_duplicate_user(db):
    auth_service = AuthService(db)
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    # First registration should succeed
    auth_service.register_user(user_data)
    
    # Second registration should fail
    with pytest.raises(ValueError, match="Username or email already exists"):
        auth_service.register_user(user_data)

def test_authenticate_user(db, test_user):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user("testuser", "testpass")
    assert user is not None
    assert user.id == test_user.id
    
    wrong_user = auth_service.authenticate_user("testuser", "wrongpass")
    assert wrong_user is None