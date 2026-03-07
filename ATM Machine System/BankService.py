class BankService:
    def __init__(self, mode="ATM"):
        self.mode=mode

    def has_sufficient_balance(self, amount, account):
        if amount > account.balance:
            return False
        return True
    
    def withdraw(self, amount, account):
        try:
            if amount <= 0:
                raise RuntimeError("Amount must be positive")
            if self.has_sufficient_balance(amount, account):
                account.balance -= amount
        except Exception as err:
            raise err
        
    def deposit(self, amount, account):
        try:
            if amount <= 0:
                raise RuntimeError("Amount must be positive")
            account.balance += amount
        except Exception as err:
            raise err
    
    def authenticate_card(self, card, pin):
        if not pin or pin != card.pin:
            return False
        return True