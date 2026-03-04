from datetime import datetime 
import threading

class Wallet:
    def __init__(self, uuid, balance=0):
        self.id = uuid
        self.balance = balance
        # self.transactions = {}    if transaction lookup is required
        self.transactions = []      # if group of transactions query is required
        self.created_at = datetime.now()
        self._lock = threading.RLock()
    
    def get_balance(self):
        return self.balance
    
    def get_transactions(self):
        res = []
        # for transaction in list(self.transactions.values()):
        for transaction in self.transactions:
            res.append(transaction.get_summary())
        return res
    
    def add_transaction(self, transaction):
        # self.transactions[transaction.id] = transaction
        self.transactions.append(transaction)
    
    def add_money(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
    
    def withdraw_money(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Amount cannot be greater than balance")
        self.balance -= amount
        