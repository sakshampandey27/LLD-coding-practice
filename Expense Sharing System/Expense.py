from enum import Enum
import uuid
from UserRepository import UserRepository

class ExpenseType(Enum):
    EQUAL = 1
    EXACT = 2
    PERCENT = 3

class Expense:
    def __init__(self, paying_user, amount, participants, expense_type, split_values=None):
        if not paying_user:
            raise ValueError("User cannot be empty")        
        self.paid_by = paying_user

        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.amount = amount

        if len(participants) < 2:
            raise ValueError("Expense must have at least 2 participants")
        self.participants = participants

        try:
            expense_type = ExpenseType[expense_type.strip().upper()]
            self.expense_type = expense_type
        except KeyError:
            raise KeyError(f"Split type must be one of these - {ExpenseType._member_names_}")
        
        if expense_type != ExpenseType.EQUAL and not split_values:
            raise ValueError("Split values must be provided for non-equal expense types")
        
        if split_values and len(split_values) != len(participants):
            raise ValueError("Exactly one split value must be provided for every participant of the expense")
        self.split_values = split_values

    
    def is_valid(self):
        if self.expense_type == ExpenseType.EXACT:
            return self.amount == sum(self.split_values)
        
        if self.expense_type == ExpenseType.PERCENT:
            return sum(self.split_values) == 100