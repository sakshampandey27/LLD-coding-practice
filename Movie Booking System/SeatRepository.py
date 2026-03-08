class SeatRepository:
    def __init__(self):
        self.seats = {}
    
    def save(self, seat):
        self.seats[seat.id] = seat
    
    def get(self, seat_id):
        if seat_id not in self.seats:
            raise KeyError("Seat not found")
        return self.seats[seat_id]

    def list(self):
        return list(self.seats.values())