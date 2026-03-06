from ExpenseRepository import ExpenseRepository
from UserRepository import UserRepository
from User import User
from Expense import Expense, ExpenseType
from ExpenseStrategy import EqualSplitStrategy, ExactSplitStrategy, PercentSplitStrategy

class ExpenseManager:
    def __init__(self):
        # self.expense_repository = ExpenseRepository()
        self.user_repository = UserRepository()
        self.expense_strategy = None

    def add_user(self, name):
        try:
            user = User(name)
            self.user_repository.save(user)
            return user.id
        except Exception as err:
            raise err

    def set_expense_strategy(self, expense_type):
        if ExpenseType[expense_type.strip().upper()] == ExpenseType.EQUAL:
            self.expense_strategy = EqualSplitStrategy()
        elif ExpenseType[expense_type.strip().upper()] == ExpenseType.EXACT:
            self.expense_strategy = ExactSplitStrategy()
        elif ExpenseType[expense_type.strip().upper()] == ExpenseType.PERCENT:
            self.expense_strategy = PercentSplitStrategy()        

    def add_expense(self, paying_user_id, amount, participant_ids, expense_type, split_values=None):
        try:
            paying_user = self.user_repository.get(paying_user_id)
            
            participants = []
            for p_id in participant_ids:
                participants.append(self.user_repository.get(p_id))

            expense = Expense(paying_user, amount, participants, expense_type, split_values)
            self.set_expense_strategy(expense_type)
            self.expense_strategy.execute(expense)
        
        except Exception as err:
            raise err

    def show_balance(self, user_id):
        try:
            user = self.user_repository.get(user_id)
            return user.balances
        except Exception as err:
            raise err
        
    def show_all_balances(self):
        result = []
        users = self.user_repository.list()

        for user in users:
            for other_user, amount in user.balances.items():
                if amount > 0:
                    result.append(f"{user.name} owes {other_user}: {amount}")

        if not result:
            return "No balances"

        return "\n".join(result)
    

if __name__ == '__main__':
    expenseManager = ExpenseManager()
    u1 = expenseManager.add_user("U1")
    u2 = expenseManager.add_user("U2")
    u3 = expenseManager.add_user("U3")
    u4 = expenseManager.add_user("U4")
    u5 = expenseManager.add_user("U5")
    expenseManager.add_expense(u1, 50, [u2, u3], "EQUAL")
    expenseManager.add_expense(u3, 30, [u4, u5], "EQUAL")
    print(expenseManager.show_balance(u1))
    print(expenseManager.show_balance(u2))
    print(expenseManager.show_balance(u3))
    print(expenseManager.show_balance(u4))
    print(expenseManager.show_balance(u5))
    expenseManager.add_expense(u5, 60, [u2, u5, u4], "EXACT", [16, 20, 24])
    expenseManager.add_expense(u4, 70, [u1, u2, u3, u4, u5], "PERCENT", [10, 20, 20, 20, 30])
    print(expenseManager.show_balance(u1))
    print(expenseManager.show_balance(u2))
    print(expenseManager.show_balance(u3))
    print(expenseManager.show_balance(u4))
    print(expenseManager.show_balance(u5))
    print(expenseManager.show_all_balances())