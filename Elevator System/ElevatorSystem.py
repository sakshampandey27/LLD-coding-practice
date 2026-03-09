class ElevatorController:
    def __init__(self):
        self.elevators = [
            Elevator(),
            Elevator(),
            Elevator()
        ]

    def request_elevator(self, floor, direction):
        if floor < 0 or floor > 9:
            return False
        if direction != Direction.UP and direction != Direction.DOWN:
            return False

        best = self.select_best_elevator(floor, direction)
        if best is None:
            return False

        type = RequestType.PICKUP_UP if direction == Direction.UP else RequestType.PICKUP_DOWN
        return best.add_request(floor, type)

    def step(self):
        for elevator in self.elevators:
            elevator.step()

    def select_best_elevator(self, floor, direction):
        best = self.find_committed_to_floor(floor, direction)
        if best is not None:
            return best

        best = self.find_nearest_idle(floor)
        if best is not None:
            return best

        return self.find_nearest(floor)

    def find_committed_to_floor(self, floor, direction):
        nearest = None
        min_distance = float('inf')

        for e in self.elevators:
            if e.get_direction() != direction:
                continue

            is_moving_toward = (
                (direction == Direction.UP and e.get_current_floor() < floor) or
                (direction == Direction.DOWN and e.get_current_floor() > floor)
            )

            if not is_moving_toward:
                continue

            if not e.has_requests_at_or_beyond(floor, direction):
                continue

            distance = abs(e.get_current_floor() - floor)
            if distance < min_distance:
                min_distance = distance
                nearest = e

        return nearest

    def find_nearest_idle(self, floor):
        nearest = None
        min_distance = float('inf')

        for e in self.elevators:
            if e.get_direction() != Direction.IDLE:
                continue

            distance = abs(e.get_current_floor() - floor)
            if distance < min_distance:
                min_distance = distance
                nearest = e

        return nearest

    def find_nearest(self, floor):
        nearest = self.elevators[0]
        min_distance = abs(self.elevators[0].get_current_floor() - floor)

        for e in self.elevators:
            distance = abs(e.get_current_floor() - floor)
            if distance < min_distance:
                min_distance = distance
                nearest = e

        return nearest
