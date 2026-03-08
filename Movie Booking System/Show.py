from Seat import Seat, SeatStatus, SeatType
from SeatRepository import SeatRepository
import threading

class Show:
    def __init__(self, id, start_time, movie_name):
        self.id = id
        self.start_time = start_time
        self.movie_name = movie_name
        self.seats = SeatRepository()
        self._lock = threading.RLock()
        self._generate_seats()
    
    def _generate_seats(self):
        for idx in range(1, 31):
            id = "S" + str(idx)
            seat = Seat(id, SeatType.REGULAR)
            self.seats.save(seat)
        for idx in range(31, 51):
            id = "S" + str(idx)
            seat = Seat(id, SeatType.PREMIUM)
            self.seats.save(seat)
        for idx in range(51, 61):
            id = "S" + str(idx)
            seat = Seat(id, SeatType.RECLINER)
            self.seats.save(seat)


    def get_movie_name(self):
        return self.movie_name

    def get_time(self):
        return self.start_time

    def get_available_seat_count(self):
        # approximate count - can change at the time of booking
        count = 0
        for seat in self.seats.list():
            if seat.is_available():
                count += 1
        return count

    def get_available_seats(self):
        available_seats = []
        for seat in self.seats.list():
            if seat.is_available():
                available_seats.append(seat.id)
        return available_seats

    def get_summary(self):
        return {
            "start_time": self.start_time,
            "movie_name": self.movie_name,
            "seats_available": self.get_available_seat_count()
        }

    def get_seats_by_id(self, seat_ids):
        seats = []
        for s_id in seat_ids:
            seat = self.seats.get(s_id)
            seats.append(seat)
        return seats
    
    def lock_seats(self, user_id, seats):
        reserved_seats = []
        try:
            for seat in seats:                
                seat.lock(user_id)
                reserved_seats.append(seat)
        except Exception as err:
            for seat in reserved_seats:
                seat.unlock()
            raise err
        finally:
            reserved_seats = []
    
    def release_seats(self, seats):
        try:
            for seat in seats:
                seat.unlock()
        except Exception as err:
            raise err