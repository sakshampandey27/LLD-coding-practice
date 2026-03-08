class BookingRepository:
    def __init__(self):
        self.bookings = {}
    
    def save(self, booking):
        self.bookings[booking.id] = booking
    
    def get(self, booking_id):
        if booking_id not in self.bookings:
            raise KeyError(f"Booking with ID = {booking_id} not found")
        return self.bookings[booking_id]
    
    def list(self):
        return list(self.bookings.values())