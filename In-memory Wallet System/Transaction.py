from enum import Enum
from datetime import datetime
import uuid

class TransactionType(Enum):
    DEBIT = 1
    CREDIT = 2
    TRANSFER = 3

class Transaction:
    def __init__(self, amount, trans_type, destination, source=None):
        self.id = str(uuid.uuid4())
        
        if amount <= 0:
            raise ValueError("Transaction amount must be positive")
        self.amount = amount
        
        if not trans_type:
            raise ValueError("Transaction type cannot be empty")
        try:
            self.type = TransactionType[trans_type.strip().upper()]
        except KeyError:
            raise KeyError("Transaction type is invalid")
        
        self.source = source.id if source else "N/A"
        self.destination = destination.id
        self.timestamp = datetime.now()

    def get_summary(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "type": self.type,
            "source": self.source if self.source else "N/A",
            "destination": self.destination,
            "timestamp": self.timestamp
        }