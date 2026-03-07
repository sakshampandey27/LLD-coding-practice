from abc import ABC, abstractmethod

class MatchingStrategy:
    @abstractmethod
    def match(self, rider, drivers):
        pass

class LocationMatchingStrategy:
    def match(self, ride, drivers):
        pickup_location = ride.get_pickup_location()
        nearest = None
        min_distance = float('inf')
        
        for driver in drivers:
            if not driver.is_available() or driver in ride.get_skipped_drivers():
                continue
            current_location = driver.get_location()
            dist = self.calculate_distance(pickup_location, current_location)
            if dist < min_distance:
                nearest = driver
                min_distance = dist
        
        return nearest

    def calculate_distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5