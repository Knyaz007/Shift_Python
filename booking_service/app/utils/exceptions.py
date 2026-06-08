class BookingError(Exception):
    """Base exception for booking errors"""
    pass

class BookingNotFoundError(BookingError):
    """Booking not found"""
    pass

class SlotNotAvailableError(BookingError):
    """Time slot is not available"""
    pass

class PermissionDeniedError(BookingError):
    """User doesn't have permission for this action"""
    pass

class ValidationError(BookingError):
    """Data validation error"""
    pass