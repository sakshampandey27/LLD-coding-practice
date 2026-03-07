from enum import Enum
import uuid
import random

class RideStatus:
    REQUESTED = 1
    ACCEPTED = 2
    IN_PROGRESS = 3
    COMPLETED = 4
    CANCELLED = 5

class Ride:
    def __init__(self, rider, pickup_location):
        self.ride_id = str(uuid.uuid4())
        self._rider = rider
        self._driver = None
        self.fare = random.randint(10,20)
        self._status = RideStatus.REQUESTED
        self.skipped_drivers = set()
        self.pickup_location = pickup_location

    def get_rider(self):
        return self._rider

    def get_driver(self):
        return self._driver
    
    def set_driver(self, driver):
        self._driver = driver

    def get_status(self):
        return self._status
    
    def set_status(self, status):
        if self._status == RideStatus.COMPLETED:
            raise RuntimeError("Ride is already completed!")
        self._status = status
        
    def add_skipped_driver(self, driver):
        self.skipped_drivers.add(driver)
    
    def get_skipped_drivers(self):
        return list(self.skipped_drivers)
    
    def get_pickup_location(self):
        return self.pickup_location

