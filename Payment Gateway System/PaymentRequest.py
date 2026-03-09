class PaymentRequest:
    def __init__(self, client_id, amount, paymode, instrument):
        self.client_id = client_id
        self.amount = amount
        self.paymode = paymode
        self.instrument = instrument
