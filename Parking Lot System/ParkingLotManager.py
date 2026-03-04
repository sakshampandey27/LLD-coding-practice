from collections import deque
import threading
from datetime import datetime
from VehicleType import VehicleType
from TicketRepository import TicketRepository
from Ticket import Ticket
from ParkingSpot import ParkingSpot, ParkingSpotType

class ParkingLotManager:
    def __init__(self, bike_count, car_count, truck_count):
        self.bike_spots_available = deque(self._initialize_bike_spots(bike_count))
        self.car_spots_available = deque(self._initialize_car_spots(car_count))
        self.truck_spots_available = deque(self._initialize_truck_spots(truck_count))
        self.ticket_repository = TicketRepository()
        self._lock = threading.RLock()

    def _initialize_bike_spots(self, count):
        res = [ParkingSpot(type=ParkingSpotType.BIKE_SPOT) for _ in range(count)]
        return res

    def _initialize_car_spots(self, count):
        return [ParkingSpot(type=ParkingSpotType.CAR_SPOT) for _ in range(count)]
    
    def _initialize_truck_spots(self, count):
        return [ParkingSpot(type=ParkingSpotType.TRUCK_SPOT) for _ in range(count)]

    def park(self, vehicle_type):
        try:
            vehicle_type = VehicleType[vehicle_type.strip().upper()]
        except Exception:
            raise ValueError("Invalid vehicle type")
        
        with self._lock:
            if vehicle_type == VehicleType.BIKE:
                ticket_id = self.park_bike()
            elif vehicle_type == VehicleType.CAR:
                ticket_id = self.park_car()
            elif vehicle_type == VehicleType.TRUCK:
                ticket_id = self.park_truck()

        return ticket_id
    
    def park_bike(self):
        if len(self.bike_spots_available) > 0:
            bike_spot = self.bike_spots_available.popleft()
            bike_spot.occupy()
            ticket = Ticket(bike_spot)
        elif len(self.car_spots_available) > 0:
            car_spot = self.car_spots_available.popleft()
            car_spot.occupy()
            ticket = Ticket(car_spot)
        else:
            raise RuntimeError("No available spots right now for bikes")
        
        self.ticket_repository.save(ticket)
        return ticket.id            

    def park_car(self):
        if len(self.car_spots_available) > 0:
            car_spot = self.car_spots_available.popleft()
            car_spot.occupy()
            ticket = Ticket(car_spot)
            self.ticket_repository.save(ticket)
            return ticket.id
        else:
            raise RuntimeError("No available spots right now for cars")
        
    def park_truck(self):
        if len(self.truck_spots_available) > 0:
            truck_spot = self.truck_spots_available.popleft()
            truck_spot.occupy()
            ticket = Ticket(truck_spot)
            self.ticket_repository.save(ticket)
            return ticket.id
        else:
            raise RuntimeError("No available spots right now for trucks")
        
    def unpark(self, ticket_id):
        with self._lock:
            try:
                ticket = self.ticket_repository.get(ticket_id)
                total_fees = ticket.calculate_fees()
                ticket.spot.vacate()
                
                if ticket.spot.type == ParkingSpotType.BIKE_SPOT:
                    self.bike_spots_available.append(ticket.spot)
                elif ticket.spot.type == ParkingSpotType.CAR_SPOT:
                    self.car_spots_available.append(ticket.spot)
                elif ticket.spot.type == ParkingSpotType.TRUCK_SPOT:
                    self.truck_spots_available.append(ticket.spot)
                
                self.ticket_repository.remove(ticket_id)
                return f"Total amount due = {total_fees}\n"
            
            except KeyError as err:
                raise err
        

    def available_spots(self, vehicle_type):
        try:
            vehicle_type = VehicleType[vehicle_type.strip().upper()]
        except Exception:
            raise ValueError("Invalid vehicle type")
        
        if vehicle_type == VehicleType.BIKE:
            return len(self.bike_spots_available)
        if vehicle_type == VehicleType.CAR:
            return len(self.car_spots_available)
        if vehicle_type == VehicleType.TRUCK:
            return len(self.truck_spots_available)

if __name__ == '__main__':
    parking = ParkingLotManager(
        bike_count=2,
        car_count=2,
        truck_count=1
    )

    print("---- Initial availability ----")
    print("Bike:", parking.available_spots("BIKE"))
    print("Car:", parking.available_spots("CAR"))
    print("Truck:", parking.available_spots("TRUCK"))


    print("\n---- Parking vehicles ----")
    t1 = parking.park("BIKE")
    print("Bike parked, ticket:", t1)

    t2 = parking.park("BIKE")
    print("Bike parked, ticket:", t2)

    t3 = parking.park("BIKE")   # should fall back to CAR spot
    print("Bike parked in car spot, ticket:", t3)

    t4 = parking.park("CAR")
    print("Car parked, ticket:", t4)

    t5 = parking.park("TRUCK")
    print("Truck parked, ticket:", t5)

    print("\n---- Availability after parking ----")
    print("Bike:", parking.available_spots("BIKE"))
    print("Car:", parking.available_spots("CAR"))
    print("Truck:", parking.available_spots("TRUCK"))

    print("\n---- Attempting overflow parking ----")
    try:
        parking.park("TRUCK")
    except Exception as e:
        print("Expected failure:", e)

    print("\n---- Unparking vehicles ----")
    fee1 = parking.unpark(t1)
    print("Bike unparked. ", fee1)

    fee2 = parking.unpark(t3)
    print("Bike (car spot) unparked. ", fee2)

    print("\n---- Availability after unparking ----")
    print("Bike:", parking.available_spots("BIKE"))
    print("Car:", parking.available_spots("CAR"))
    print("Truck:", parking.available_spots("TRUCK"))

    print("\n---- Invalid ticket test ----")
    try:
        parking.unpark("INVALID_TICKET")
    except Exception as e:
        print("Expected error:", e)

    print("\n---- Re-parking after spots freed ----")
    t6 = parking.park("CAR")
    print("Car parked again, ticket:", t6)

    t7 = parking.park("BIKE")
    print("Bike parked again, ticket:", t7)

    print("\n---- Final availability ----")
    print("Bike:", parking.available_spots("BIKE"))
    print("Car:", parking.available_spots("CAR"))
    print("Truck:", parking.available_spots("TRUCK"))