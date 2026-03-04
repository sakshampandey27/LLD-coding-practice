class WalletRepository:
    def __init__(self):
        self.wallets = {}
    
    def save(self, wallet):
        self.wallets[wallet.id] = wallet
    
    def get(self, wallet_id):
        if wallet_id not in self.wallets:
            raise KeyError("Wallet does not exist")
        return self.wallets[wallet_id]    
    
    def list(self):
        return list(self.wallets.values())