import threading
from collections import deque
from Ride import RideStatus

class Driver:
    def __init__(self, id, location):
        self.id = id
        self._is_online = True
        self._location = location
        self._lock = threading.RLock()
        self._current_ride = None

    def set_driver_availability(self, is_online):
        if self._current_ride:
            raise RuntimeError("Cannot modify driver availability while serving a ride")
        self._is_online = is_online
    
    def is_available(self):
        return self._is_online == True and not self._current_ride
    
    def update_location(self, location):
        if self._current_ride:
            raise RuntimeError("Cannot modify driver location while serving a ride")
        self._location = location
    
    def get_location(self):
        return self._location
    
    def accept_ride(self, ride):
        if not self._is_online:
            raise RuntimeError("Cannot accept a ride while offline")
        if self._current_ride:
            raise RuntimeError("Cannot accept a ride while actively serving another ride")
        if ride.get_status() != RideStatus.REQUESTED:
            raise RuntimeError("Can only accept a ride that is being requested")
        self._current_ride = ride

    def start_ride(self):
        if not self._current_ride:
            raise RuntimeError("No current ride found to complete")
        if self._current_ride.get_status() != RideStatus.ACCEPTED:
            raise RuntimeError("Can only start a ride that is accepted")
        

    def complete_ride(self):
        if not self._current_ride:
            raise RuntimeError("No current ride found to complete")
        if self._current_ride.get_status() != RideStatus.IN_PROGRESS:
            raise RuntimeError("Can only complete a ride that is in progress")
        self._current_ride = None

    def cancel_ride(self):
        if not self._current_ride:
            raise RuntimeError("No current ride found to cancel")
        if self._current_ride.get_status() != RideStatus.ACCEPTED:
            raise RuntimeError("Can only cancel a ride that is accepted")
        self._current_ride = None
