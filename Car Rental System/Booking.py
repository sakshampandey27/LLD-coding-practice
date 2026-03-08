from enum import Enum
from datetime import datetime, timedelta
import uuid

class BookingStatus(Enum):
    CREATED = 1
    RESERVED = 2
    ACTIVE = 3
    COMPLETED = 4
    CANCELLED = 5
    
class Booking:
    def __init__(self, user, car, ):
        self.id = str(uuid.uuid4())
        self.user = user
        self.car = car
        self._status = BookingStatus.CREATED
        self.created_at = datetime.now()

    def _is_expired(self):
        return datetime.now() > self.created_at + timedelta(seconds=5)
    
    def get_user(self):
        return self.user
    
    def get_car(self):
        if self._is_expired():
            raise RuntimeError("Booking expired!")
        return self.car
    
    def reserve(self):
        if self._status != BookingStatus.CREATED:
            raise RuntimeError("You can only reserve a booking in created state.")
        if self._is_expired():
            raise RuntimeError("Booking expired!")
        self._status = BookingStatus.RESERVED
    
    def begin(self):
        if self._status != BookingStatus.RESERVED:
            raise RuntimeError("You can only start a booking in reserved state.")
        if self._is_expired():
            raise RuntimeError("Booking expired!")
        self._status = BookingStatus.ACTIVE
    
    def end(self):
        if self._status != BookingStatus.ACTIVE:
            raise RuntimeError("You can only complete a booking in active state.")
        self._status = BookingStatus.COMPLETED

    def cancel(self):
        if self._status not in [BookingStatus.CREATED, BookingStatus.RESERVED]:
            raise RuntimeError("You can only reserve a booking in created or reserved state.")
        if self._is_expired():
            raise RuntimeError("Booking expired!")
        self._status = BookingStatus.CANCELLED
        

    