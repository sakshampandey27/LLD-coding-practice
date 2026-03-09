class Client:
    def __init__(self, id, name, supported_paymodes):
        self.id = id
        self.name = name
        self.supported_paymodes = set(supported_paymodes)
    
    def get_supported_paymodes(self):
        return sorted(list(self.supported_paymodes), key=lambda x: x.value)
    
    def get_summary(self):
        return {
            "Name": self.name,
            "Supported Paymodes": self.get_supported_paymodes()
        }
    
    def add_paymode(self, paymode):
        self.supported_paymodes.add(paymode)
    
    def remove_paymode(self, paymode):
        self.supported_paymodes.remove(paymode)
    
    def validate_paymode_support(self, paymode):
        return paymode in self.supported_paymodes