class RiderRepository:
    def __init__(self):
        self.riders = {}
    
    def get(self, rider_id):
        if rider_id not in self.riders:
            raise KeyError(f"Rider with {rider_id} not found")
        return self.riders[rider_id]
    
    def save(self, rider):
        self.riders[rider.id] = rider
    
    def list(self):
        return list(self.riders.values())