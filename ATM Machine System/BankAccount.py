import uuid

class BankAccount:
    def __init__(self, balance=0):
        self.account_id = str(uuid.uuid4())
        self.balance = balance
    
    def get_balance(self):
        return self.balance
        

    
    