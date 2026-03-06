import random

class Player:
    def __init__(self, name, start_position=0):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        if not isinstance(start_position, int):
            raise ValueError("Start position must be integer")
        self.position = start_position
    
    def play(self):
        dice_roll = random.randint(1,6)
        return dice_roll
    