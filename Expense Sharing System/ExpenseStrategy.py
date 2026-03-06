from abc import ABC, abstractmethod
from decimal import getcontext, Decimal

getcontext().prec = 2

class SplitStrategy(ABC):
    @abstractmethod
    def execute(self, expense):
        pass

class EqualSplitStrategy(SplitStrategy):
    def execute(self, expense):
        count = len(expense.participants)
        share = Decimal(expense.amount / count)
        payer = expense.paid_by

        for user in expense.participants:
            if user == payer:
                continue
            user.balances[payer.name] = user.balances.get(payer.name, 0) + share
            payer.balances[user.name] = payer.balances.get(user.name, 0) - share
        

class ExactSplitStrategy(SplitStrategy):
    def execute(self, expense):
        try:
            if not expense.is_valid():
                raise RuntimeError("Invalid expense!")
            payer = expense.paid_by
            for user, share in zip(expense.participants, expense.split_values):
                if user==payer:
                    continue
                user.balances[payer.name] = user.balances.get(payer.name, 0) + Decimal(share)
                payer.balances[user.name] = payer.balances.get(user.name, 0) - Decimal(share)
        
        except Exception as err:
            raise err
        
class PercentSplitStrategy(SplitStrategy):
    def execute(self, expense):
        try:
            if not expense.is_valid():
                raise RuntimeError("Invalid expense!")
            payer = expense.paid_by
            for user, share in zip(expense.participants, expense.split_values):
                if user==payer:
                    continue
                share = Decimal(share * expense.amount / 100)
                user.balances[payer.name] = user.balances.get(payer.name, 0) + share
                payer.balances[user.name] = payer.balances.get(user.name, 0) - share
        
        except Exception as err:
            raise err
