import uuid

class Booking:
    def __init__(self, user_id, show, seats):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.show = show
        self.seats = seats
    
    def get_summary(self):
        return {
            "User": self.user_id,
            "Movie": self.show.get_movie_name(),
            "Time": self.show.get_time(),
            "Seats": [seat.id for seat in self.seats]
        }