import uuid
from datetime import datetime, timedelta
from math import ceil

class Ticket:
    def __init__(self, spot):
        self.id = str(uuid.uuid4())
        self.entry_time = datetime.now()
        self.fee = 10
        self.spot = spot
    
    def calculate_fees(self):
        total_seconds = (datetime.now() - self.entry_time) / timedelta(seconds=1)
        return ceil(total_seconds) * self.fee
    
    