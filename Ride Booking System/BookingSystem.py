from DriverRepository import DriverRepository
from RiderRepository import RiderRepository
from Driver import Driver
from Rider import Rider
from Ride import Ride, RideStatus
from MatchingStrategy import LocationMatchingStrategy

class RideBookingSystem:
    def __init__(self):
        self.driver_repository = DriverRepository()
        self.rider_repository = RiderRepository()
        self._strategy = LocationMatchingStrategy()

    def set_strategy(self, strategy):
        self._strategy = strategy

    def registerDriver(self, driver_id, location):
        try:
            driver = Driver(driver_id, location)
            self.driver_repository.save(driver)
        except Exception as err:
            raise err

    def registerRider(self, rider_id):
        try:
            rider = Rider(rider_id)
            self.rider_repository.save(rider)
        except Exception as err:
            raise err
        
    def updateDriverLocation(self, driver_id, location):
        try:
            driver = self.driver_repository.get(driver_id)
            driver.update_location(location)
        except Exception as err:
            raise err

    def setDriverAvailability(self, driver_id, is_online):
        try:
            driver = self.driver_repository.get(driver_id)
            driver.set_driver_availability(is_online)
        except Exception as err:
            raise err

    def requestRide(self, rider_id, pickup_location):
        try:
            rider = self.rider_repository.get(rider_id)
            ride = Ride(rider, pickup_location)
            matched_driver = self._match_ride_to_driver(ride)
            return ride, matched_driver
        except Exception as err:
            raise err
    
    def findAnotherDriver(self, ride):
        try:
            matched_driver = self._match_ride_to_driver(ride)
            return matched_driver
        except Exception as err:
            raise err
        
    def _match_ride_to_driver(self, ride):
        try:
            drivers = self.driver_repository.list()
            nearest = self._strategy.match(ride, drivers)
            return nearest
        except Exception as err:
            raise err
        
    def acceptRide(self, driver, ride):
        try:
            with driver._lock:
                driver.accept_ride(ride)
                ride.set_status(RideStatus.ACCEPTED)
                ride.set_driver(driver)
        except Exception as err:
            raise err

    def rejectRide(self, driver, ride):
        try:            
            ride.add_skipped_driver(driver)
        except Exception as err:
            raise err

    def startRide(self, ride):
        try:            
            driver = ride.get_driver()
            with driver._lock:
                driver.start_ride()
                ride.set_status(RideStatus.IN_PROGRESS)
        except Exception as err:
            raise err

    def completeRide(self, ride):
        try:            
            driver = ride.get_driver()
            with driver._lock:
                driver.complete_ride()
                ride.set_status(RideStatus.COMPLETED)
        except Exception as err:
            raise err
    
    def cancelRide(self, ride):
        try:            
            driver = ride.get_driver()
            with driver._lock:
                driver.cancel_ride()
                ride.set_status(RideStatus.CANCELLED)
        except Exception as err:
            raise err



if __name__ == '__main__':
    rideBookingSystem = RideBookingSystem()
    rideBookingSystem.registerDriver("D1", (0,0))
    rideBookingSystem.registerDriver("D2", (5,5))
    rideBookingSystem.registerDriver("D3", (10,10))
    rideBookingSystem.registerRider("R1")
    rideBookingSystem.registerRider("R2")
    ride1, matched_driver = rideBookingSystem.requestRide("R1", (1,1))
    rideBookingSystem.rejectRide(matched_driver, ride1)
    matched_driver = rideBookingSystem.findAnotherDriver(ride1)
    rideBookingSystem.acceptRide(matched_driver, ride1)
    rideBookingSystem.startRide(ride1)
    rideBookingSystem.completeRide(ride1)