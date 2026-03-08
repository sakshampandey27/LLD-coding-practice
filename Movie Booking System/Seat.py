from enum import Enum
from datetime import datetime, timedelta

class SeatType(Enum):
    REGULAR = 1
    PREMIUM = 2
    RECLINER = 3

class SeatStatus(Enum):
    AVAILABLE = 1
    LOCKED = 2
    RESERVED = 3

class Seat:
    def __init__(self, id, seat_type):
        self.id = id
        self.type = seat_type
        self._status = SeatStatus.AVAILABLE
        self._locked_by = None
        self._locked_time = None

    def is_available(self):
        self.expiry_check()
        return self._status == SeatStatus.AVAILABLE

    def is_locked(self):
        self.expiry_check()
        return self._status == SeatStatus.LOCKED
    
    def expiry_check(self):
        # 5 second limit for simulation
        if self._status == SeatStatus.LOCKED and datetime.now() > self._locked_time + timedelta(seconds=5):
            self._locked_by = None
            self._locked_time = None
            self._status = SeatStatus.AVAILABLE
        
    def lock(self, user_id):
        if not self.is_available():
            raise RuntimeError(f"Seat {self.id} is not available")
        self._locked_by = user_id
        self._locked_time = datetime.now()
        self._status = SeatStatus.LOCKED
    
    def unlock(self, user_id):
        if self._status == SeatStatus.AVAILABLE:
            raise ValueError("Seat is already unlocked")
        if self.get_user_who_locked() != user_id:
            raise ValueError("Seat can only be unlocked by the person who locked it")
        self._status = SeatStatus.AVAILABLE
        self._locked_by = None
        self._locked_time = None
    
    def reserve(self):
        if self._status == SeatStatus.RESERVED:
            raise ValueError("Seat is already reserved")
        if self._status == SeatStatus.AVAILABLE:
            raise ValueError("Seat must be locked first")
        self._status = SeatStatus.RESERVED
        self._locked_by = None
        self._locked_time = None

    def get_user_who_locked(self):
        if self.is_locked():
            return self._locked_by
        
