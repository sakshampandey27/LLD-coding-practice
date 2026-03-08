from enum import Enum
import threading

class CarStatus(Enum):
    AVAILABLE = 1
    RESERVED = 2

class Car:
    def __init__(self, id, model, year, location, pricePerHour):
        self.id = id
        self.model = model
        self.year = year
        self.location = location
        self.pricePerHour = pricePerHour
        self._status = CarStatus.AVAILABLE
        self._lock = threading.RLock()
    
    def is_available(self):
        return self._status == CarStatus.AVAILABLE
    
    def mark_reserved(self):
        self._status = CarStatus.RESERVED
    
    def mark_available(self):
        self._status = CarStatus.AVAILABLE
    
    def get_location(self):
        return self.location
    
    def get_summary(self):
        return {
            "Model": self.model,
            "Year": self.year,
            "Location": self.location,
            "Price": self.pricePerHour
        }