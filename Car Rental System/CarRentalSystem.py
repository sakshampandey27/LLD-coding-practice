from User import User
from Car import Car, CarStatus
from Booking import Booking
from CarRepository import CarRepository
from BookingRepository import BookingRepository
import time

class CarRentalSystem:
    def __init__(self):
        self.car_repository = CarRepository()
        self.booking_repository = BookingRepository()
        self.users = {}

    def registerCar(self, carId, model, year, location, pricePerHour):
        try:
            car = Car(carId, model, year, location, pricePerHour)
            self.car_repository.save(car)
        except Exception as err:
            raise err
    
    def registerUser(self, userId):
        try:
            user = User(userId)
            self.users[userId] = user
        except Exception as err:
            raise err
        
    def searchCars(self, location):
        try:
            all_cars = self.car_repository.list()
            filtered_cars = []
            for car in all_cars:
                if car.is_available() and car.get_location() == location:
                    filtered_cars.append(car.get_summary())
            return filtered_cars
        except Exception as err:
            raise err

    def reserveCar(self, userId, carId):
        try:
            if userId not in self.users:
                raise KeyError(f"User with ID = {userId} does not exist")
            user = self.users[userId]
            car = self.car_repository.get(carId)
            with car._lock:
                if car.is_available():
                    booking = Booking(user, car)
                    self.booking_repository.save(booking)
                    booking.reserve()
                    car.mark_reserved()
            return booking.id
        except Exception as err:
            raise err

    def cancelBooking(self, userId, bookingId):
        try:
            if userId not in self.users:
                raise KeyError(f"User with ID = {userId} does not exist")
            booking = self.booking_repository.get(bookingId)
            if userId != booking.get_user().id:
                raise RuntimeError(f"Users can only cancel their own bookings")
            car = booking.get_car()
            with car._lock:
                booking.cancel()
                car.mark_available()
            return f"Booking with ID = {bookingId} cancelled!"
        except Exception as err:
            raise err

    def startRental(self, userId, bookingId):
        try:
            if userId not in self.users:
                raise KeyError(f"User with ID = {userId} does not exist")
            booking = self.booking_repository.get(bookingId)
            if userId != booking.get_user().id:
                raise RuntimeError(f"Users can only activate their own bookings")
            booking.begin()
            return f"Booking with ID = {bookingId} started!"
        except Exception as err:
            raise err

    def endRental(self, userId, bookingId):
        try:
            if userId not in self.users:
                raise KeyError(f"User with ID = {userId} does not exist")
            booking = self.booking_repository.get(bookingId)
            if userId != booking.get_user().id:
                raise RuntimeError(f"Users can only end their own bookings")
            car = booking.get_car()
            with car._lock:
                booking.end()
                car.mark_available()             
            return f"Booking with ID = {bookingId} completed!"   
        except Exception as err:
            raise err

if __name__ == '__main__':
    carSystem = CarRentalSystem()
    carSystem.registerCar("C1", "Toyota Camry ", "2025", "Raleigh", 100)
    carSystem.registerCar("C2", "Maruti 800 ", "2024", "Seattle", 40)
    carSystem.registerCar("C3", "Tesla X ", "2023", "Raleigh", 250)
    carSystem.registerCar("C4", "Honda Amaze ", "2026", "Raleigh", 90)
    carSystem.registerUser("U1")
    carSystem.registerUser("U2")
    carSystem.registerUser("U3")

    print(carSystem.searchCars("Raleigh"))
    b1 = carSystem.reserveCar("U1", "C4")
    print(carSystem.searchCars("Raleigh"))
    print(carSystem.startRental("U1", b1))
    b2 = carSystem.reserveCar("U2", "C3")
    print(carSystem.searchCars("Raleigh"))
    print(carSystem.cancelBooking("U2", b2))
    print(carSystem.searchCars("Raleigh"))
    print(carSystem.endRental("U1", b1))
    print(carSystem.searchCars("Raleigh"))
    print(carSystem.searchCars("Seattle"))

