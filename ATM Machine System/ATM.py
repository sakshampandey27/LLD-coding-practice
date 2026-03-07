from BankService import BankService
import threading

class Inventory:
    def __init__(self, denominations):
        self.notes = denominations

class ATM:
    def __init__(self, denominations):
        self.inventory = Inventory(denominations)
        self.bank_service = BankService()
        self._lock = threading.RLock()
        self._current_card = None
        self._is_card_authenticated = False

    def set_current_card(self, card):
        self._current_card = card
        self._is_card_authenticated = False

    def get_current_card(self):
        return self._current_card
    
    def is_card_authenticated(self):
        return self._is_card_authenticated
    
    def authenticate_card(self, card, pin):
        try:
            if not self.bank_service.authenticate_card(card, pin):
                raise RuntimeError("Could not authenticate card")
            else:
                self._is_card_authenticated = True
                return True
        except Exception as err:
            raise err

    def check_balance(self, card):
        try:            
            return card.account.get_balance()
        except Exception as err:
            raise err
        
    def deposit(self, card, denominations):
        try:
            with self._lock:
                # card = self.card_repository.get(cardNumber)
                self._validate_denomination_amounts(denominations)
                
                amount = 0
                for k, v in denominations.items():
                    self.inventory.notes[k] += v
                    amount += k * v
                                
                self.bank_service.deposit(amount, card.account)
                return amount
        except Exception as err:
            for k, v in denominations.items():
                self.inventory.notes[k] -= v
            raise err
            

    def withdraw(self, card, amount):
        try:
            withdrawn_notes = {}
            with self._lock:
                if not self.bank_service.has_sufficient_balance(amount, card.account):
                    raise RuntimeError("Insufficient balance in the account")
                
                temp_amount = amount
                withdrawn_notes = {}
                for deno in sorted(self.inventory.notes.keys(), reverse=True):
                    available = min(self.inventory.notes[deno], temp_amount // deno)
                    temp_amount -= available * deno
                    withdrawn_notes[deno] = available
                    self.inventory.notes[deno] -= available
                
                if temp_amount != 0:                    
                    raise RuntimeError("Amount cannot be withdrawn from the available cash in the machine")                
                
                self.bank_service.withdraw(amount, card.account)
                return withdrawn_notes
        except Exception as err:
            for k, v in withdrawn_notes.items():
                self.inventory.notes[k] += v
            raise err            

    def _validate_denomination_amounts(self, denominations):
        for k, v in denominations.items():
            if k not in self.inventory.notes:
                raise KeyError(f"Can only deposit {list(self.inventory.notes.keys())} notes")
            if v < 0:
                raise KeyError(f"Cannot deposit negative amount of notes for any denomination")