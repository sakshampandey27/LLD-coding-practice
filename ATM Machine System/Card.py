import random

class Card:
    def __init__(self, pin, account):
        self.cardNumber = random.randint(10**15, (10**16) - 1)
        self.pin = pin
        self.account = account
     