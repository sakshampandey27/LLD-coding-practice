class ExpenseRepository:
    def __init__(self):
        self.expenses = {}
    
    def save(self, expense):
        self.expenses[expense.id] = expense
    
    def get(self, expense_id):
        if expense_id not in self.expenses:
            raise KeyError("Expense does not exist")
        return self.expenses[expense_id]
    
    def list(self):
        return list(self.expenses.values())