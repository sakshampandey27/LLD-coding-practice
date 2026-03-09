from abc import ABC, abstractmethod
from enum import Enum

class Paymode(Enum):
    UPI = 1
    CARD = 2
    NETBANKING = 3

class PaymentInstrument(ABC):
    @abstractmethod
    def validate(self):
        pass


class UPIInstrument(PaymentInstrument):
    def __init__(self, pay_details):
        self.paymode = Paymode.UPI
        self.pay_details = pay_details
        # if not self.validate(pay_details):
        #     raise RuntimeError("Pay details not found for this payment instrument")
    
    def validate(self):
        if 'vpa' not in self.pay_details:
            return False
        self.vpa = self.pay_details['vpa']
        return True
    
    def get_paymode(self):
        return self.paymode


class CardInstrument(PaymentInstrument):
    def __init__(self, pay_details):
        self.paymode = Paymode.CARD
        self.pay_details = pay_details
        # if not self.validate(pay_details):
        #     raise RuntimeError("Pay details not found for this payment instrument")
    
    def validate(self):
        if 'card_number' not in self.pay_details:
            return False
        if 'expiry' not in self.pay_details:
            return False
        if 'cvv' not in self.pay_details:
            return False
        self.card_number = self.pay_details['card_number']
        self.expiry = self.pay_details['expiry']
        self.cvv = self.pay_details['cvv']
        return True

    def get_paymode(self):
        return self.paymode

class NetbankingInstrument(PaymentInstrument):
    def __init__(self, pay_details):
        self.paymode = Paymode.NETBANKING
        self.pay_details = pay_details
        # if not self.validate(pay_details):
        #     raise RuntimeError("Pay details not found for this payment instrument")
    
    def validate(self):
        if 'username' not in self.pay_details:
            return False
        if 'password' not in self.pay_details:
            return False
        self.username = self.pay_details['username']
        self.password = self.pay_details['password']
        return True
    
    def get_paymode(self):
        return self.paymode

        

