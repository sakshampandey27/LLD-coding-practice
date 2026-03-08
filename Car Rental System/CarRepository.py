class CarRepository:
    def __init__(self):
        self.cars = {}
    
    def save(self, car):
        self.cars[car.id] = car
    
    def get(self, car_id):
        if car_id not in self.cars:
            raise KeyError(f"Car with ID = {car_id} not found")
        return self.cars[car_id]
    
    def list(self):
        return list(self.cars.values())