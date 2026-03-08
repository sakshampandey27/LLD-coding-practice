from ShowRepository import ShowRepository
from Show import Show
from Booking import Booking
import time

class BookingService:
    def __init__(self):
        self.shows = ShowRepository()
        self.bookings = {}

    def createShow(self, show_id, start_time, movie_name):
        try:
            show = Show(show_id, start_time, movie_name)
            self.shows.save(show)
        except Exception as err:
            raise err

    def searchShows(self, movie_name):
        try:
            show_list = self.shows.list()
            result_shows = []
            for show in show_list:
                if show.get_movie_name() == movie_name:
                    result_shows.append(show.get_summary())
            return result_shows
        except Exception as err:
            raise err

    def getAvailableSeats(self, show_id):
        try:
            show = self.shows.get(show_id)
            return show.get_available_seats()
        except Exception as err:
            raise err

    def lockSeats(self, user_id, show_id, seat_ids):
        try:
            show = self.shows.get(show_id)
            with show._lock:
                seats = show.get_seats_by_id(seat_ids)
                show.lock_seats(user_id, seats)
                print("Seats locked! Book quickly before the seats are released!")
        except Exception as err:
            raise err

    def confirmBooking(self, user_id, show_id, seat_ids):
        try:
            show = self.shows.get(show_id)
            with show._lock:
                seats = show.get_seats_by_id(seat_ids)
                for seat in seats:
                    if not seat.is_locked():
                        raise RuntimeError(f"Seat {seat.id} is not locked")
                    if seat.get_user_who_locked() != user_id:
                        raise RuntimeError(f"Seat {seat.id} is locked by someone else")
                    seat.reserve()
                booking = Booking(user_id, show, seats)
                self.bookings[booking.id] = booking
                return booking.id
        except Exception as err:
            raise err

    def cancelBooking(self, booking_id):
        try:
            if booking_id not in self.bookings:
                raise KeyError("Booking not found")
            show = self.bookings[booking_id].show
            seats = self.bookings[booking_id].seats
            show.release_seats(seats)
            del self.bookings[booking_id]
        except Exception as err:
            raise err



if __name__ == '__main__':
    bookingService = BookingService()
    bookingService.createShow("SH1", "9AM", "Dhurandhar")
    bookingService.createShow("SH2", "12PM", "DDLJ")
    bookingService.createShow("SH3", "3PM", "DDLJ")
    bookingService.createShow("SH4", "6PM", "Dhurandhar")
    bookingService.createShow("SH5", "9PM", "Dhurandhar")
    print(bookingService.searchShows("Dhurandhar"))

    print(bookingService.getAvailableSeats("SH4"))
    bookingService.lockSeats("SP", "SH4", ["S1", "S2", "S3", "S4"])
    bookingService.lockSeats("SD", "SH4", ["S32", "S33", "S34", "S35"])
    print(bookingService.getAvailableSeats("SH4"))

    booking1 = bookingService.confirmBooking("SP", "SH4", ["S1", "S2", "S3", "S4"])
    print(f"Booking confirmed! - {bookingService.bookings[booking1].get_summary()}")
    booking2 = bookingService.confirmBooking("SD", "SH4", ["S32", "S33", "S34"])
    print(f"Booking confirmed! - {bookingService.bookings[booking2].get_summary()}")
    time.sleep(5)
    print(bookingService.getAvailableSeats("SH4"))
