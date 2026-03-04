from enum import Enum
import uuid

class ParkingSpotType(Enum):
    BIKE_SPOT = 1
    CAR_SPOT = 2
    TRUCK_SPOT = 3

class ParkingSpot:
    def __init__(self, type, occupied=False):
        self.id = str(uuid.uuid4())
        self.type = type
        self.occupied = occupied
    
    def is_occupied(self):
        return self.occupied
    
    def occupy(self):
        self.occupied = True
    
    def vacate(self):
        self.occupied = False