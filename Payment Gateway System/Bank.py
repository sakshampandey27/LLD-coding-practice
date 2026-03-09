import random

class Bank:
    def __init__(self, name):
        self.name = name
    
    def process_payment(self):
        return random.randint(0,1)