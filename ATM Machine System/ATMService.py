from ATM import ATM
from Card import Card
from BankAccount import BankAccount

class ATMService:
    def __init__(self, atm_denominations):
        self.ATM = ATM(atm_denominations)
        
    def insertCard(self, card, pin):
        try:
            self.ATM.set_current_card(card)
            return self.ATM.authenticate_card(card, pin)
        except Exception as err:
            raise err

    def checkBalance(self, card):
        try:
            if card != self.ATM.get_current_card() or not self.ATM.is_card_authenticated():
                raise RuntimeError("Wrong card inserted, first authenticate with this new card")
            return self.ATM.check_balance(card)
        except Exception as err:
            raise err

    def deposit(self, card, denominations):
        try:
            if card != self.ATM.get_current_card() or not self.ATM.is_card_authenticated():
                raise RuntimeError("Wrong card inserted, first authenticate with this new card")
            amount = self.ATM.deposit(card, denominations)
            return f"{amount} deposited in the account."
        except Exception as err:
            raise err
    
    def withdraw(self, card, amount):
        try:
            if card != self.ATM.get_current_card() or not self.ATM.is_card_authenticated():
                raise RuntimeError("Wrong card inserted, first authenticate with this new card")
            withdrawn_notes = self.ATM.withdraw(card, amount)
            return f"{amount} withdrawn from the account in the form of {withdrawn_notes}. "
        except Exception as err:
            raise err


if __name__ == '__main__':
    atmService = ATMService({
            2000: 1,
            500: 3,
            100: 10
        })
    
    account1 = BankAccount(5000)
    account2 = BankAccount(3500)
    account3 = BankAccount(1800)
    card1 = Card("1111", account1)
    card2 = Card("2222", account2)
    card3 = Card("3333", account3)

    atmService.insertCard(card1, "1111")
    print(atmService.checkBalance(card1))
    atmService.insertCard(card2, "2222")
    print(atmService.checkBalance(card2))
    atmService.insertCard(card3, "3333")
    print(atmService.checkBalance(card3))

    atmService.insertCard(card1, "1111")
    print(atmService.withdraw(card1, 2700))
    print(atmService.checkBalance(card1))

    atmService.insertCard(card2, "2222")
    print(atmService.withdraw(card2, 800))
    print(atmService.checkBalance(card2))

    atmService.insertCard(card3, "3333")
    print(atmService.withdraw(card3, 1000))
    print(atmService.checkBalance(card3))

    atmService.insertCard(card1, "1111")
    print(atmService.deposit(card1, {500: 3}))
    atmService.insertCard(card2, "2222")
    print(atmService.deposit(card2, {2000: 1}))
    atmService.insertCard(card3, "3333")
    print(atmService.deposit(card3, {500: 4}))

    atmService.insertCard(card1, "1111")
    print(atmService.checkBalance(card1))
    atmService.insertCard(card2, "2222")
    print(atmService.checkBalance(card2))
    atmService.insertCard(card3, "3333")
    print(atmService.checkBalance(card3))