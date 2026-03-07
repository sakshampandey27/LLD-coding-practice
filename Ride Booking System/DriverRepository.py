class DriverRepository:
    def __init__(self):
        self.drivers = {}
    
    def get(self, driver_id):
        if driver_id not in self.drivers:
            raise KeyError(f"Driver with {driver_id} not found")
        return self.drivers[driver_id]
    
    def save(self, driver):
        self.drivers[driver.id] = driver
    
    def list(self):
        return list(self.drivers.values())