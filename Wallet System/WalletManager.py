from Wallet import Wallet
from WalletRepository import WalletRepository
from Transaction import Transaction, TransactionType
import uuid
import threading

class WalletManager:
    def __init__(self):
        self.repository = WalletRepository()
        self._lock = threading.RLock()

    def _generate_uuid(self):
        return str(uuid.uuid4())
    
    def create_wallet(self, balance=0):
        with self._lock:
            try:
                wallet_id = self._generate_uuid()
                wallet = Wallet(wallet_id, balance)
                self.repository.save(wallet)
                return wallet_id
            except Exception as err:
                raise err

    def add_money(self, wallet_id, amount):
        try:
            wallet = self.repository.get(wallet_id)
            with wallet._lock:
                wallet.add_money(amount)
                transaction = Transaction(amount, trans_type="CREDIT", destination=wallet)
                wallet.add_transaction(transaction)
            return f"Transaction successful. {amount} added to {wallet_id}\n"
        except Exception as err:
            raise err
        
    def transfer_money(self, from_wallet, to_wallet, amount):
        try:
            if from_wallet == to_wallet:
                raise ValueError("Source and Destination must be different")
            
            source_wallet = self.repository.get(from_wallet)
            destination_wallet = self.repository.get(to_wallet)
            first_wallet = self.repository.get(min(from_wallet, to_wallet))
            second_wallet = self.repository.get(max(from_wallet, to_wallet))

            with first_wallet._lock:
                with second_wallet._lock:
                    source_wallet.withdraw_money(amount)
                    destination_wallet.add_money(amount)
                    transaction = Transaction(amount, trans_type="TRANSFER", destination=destination_wallet, source=source_wallet)
                    source_wallet.add_transaction(transaction)
                    destination_wallet.add_transaction(transaction)
            return f"Transaction successful. {amount} transferred from {from_wallet} to {to_wallet}\n"
        except Exception as err:
            raise err

    def get_balance(self, wallet_id):
        try:
            wallet = self.repository.get(wallet_id)
            with wallet._lock:
                balance = wallet.get_balance()
            return f"Wallet {wallet_id} has balance = {balance}\n"
        except Exception as err:
            raise err

    def get_transactions(self, wallet_id):
        try:
            wallet = self.repository.get(wallet_id)
            transactions = wallet.get_transactions()
            return f"Wallet {wallet_id} has the following transactions: \n{transactions}\n"
        except KeyError as err:
            raise err
        
    def get_transactions_advanced(self, wallet_id, limit=10, offset=0, type=None):
        try:
            wallet = self.repository.get(wallet_id)
            transactions = wallet.get_transactions()
            if type:
                transactions = [txn for txn in transactions if txn["type"] == TransactionType[type.strip().upper()]]
            transactions = transactions[offset: offset+limit]
            return f"Wallet {wallet_id} has the following transactions: \n{transactions}\n"
        except KeyError as err:
            raise err

if __name__ == '__main__':
    walletManager = WalletManager()
    wallet1 = walletManager.create_wallet(balance=50)
    wallet2 = walletManager.create_wallet(balance=100)
    print(walletManager.get_balance(wallet1))
    print(walletManager.get_balance(wallet2))
    print(walletManager.add_money(wallet1, 10))
    print(walletManager.get_transactions(wallet1))
    print(walletManager.get_balance(wallet1))
    print(walletManager.get_balance(wallet2))
    print(walletManager.transfer_money(wallet2, wallet1, 15))
    print(walletManager.get_transactions(wallet1))
    print(walletManager.get_transactions(wallet2))
    print(walletManager.get_balance(wallet1))
    print(walletManager.get_balance(wallet2))
    print(walletManager.get_transactions_advanced(wallet1, type="CREDIT"))
    print(walletManager.get_transactions_advanced(wallet2))