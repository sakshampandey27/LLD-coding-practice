from Ride import Ride, RideStatus

class Rider:
    def __init__(self, id):
        self.id = id
        self.ride_history = []
    
    def add_ride_to_history(self, ride):
        self.ride_history.append(ride)
    
    def get_ride_history(self):
        return self.ride_history