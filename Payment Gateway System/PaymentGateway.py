from Client import Client
from ClientRepository import ClientRepository
from PaymentInstrument import PaymentInstrument, UPIInstrument, CardInstrument, NetbankingInstrument, Paymode
from Router import Router
from RoutingStrategy import MappingRoutingStrategy, WeightedRoutingStrategy
from Bank import Bank
from PaymentRequest import PaymentRequest

class PaymentGateway:
    def __init__(self, supported_paymodes):
        self.client_repository = ClientRepository()
        self.supported_paymodes = set(supported_paymodes)
        self.router = Router()
    
    def add_client(self, id, name, supported_paymodes):
        try:
            for paymode in supported_paymodes:
                if paymode not in self.supported_paymodes:
                    raise RuntimeError("Paymode is not supported by the Payment Gateway")
            client = Client(id, name, supported_paymodes)
            self.client_repository.save(client)
            return client.id
        except Exception as err:
            raise err
    
    def remove_client(self, client_id):
        try:
            self.client_repository.remove(client_id)            
        except Exception as err:
            raise err

    def has_client(self, client_id):
        try:
            client = self.client_repository.get(client_id)
            return client.get_summary()
        except KeyError:
            return None
        except Exception as err:
            raise err

    def list_supported_paymodes(self, client_id=None):
        try:
            if client_id:
                client = self.client_repository.get(client_id)
                return client.get_supported_paymodes()
            else:
                return sorted(list(self.supported_paymodes), key=lambda x: x.value)
        except Exception as err:
            raise err
    
    def add_paymode_support(self, paymode, client_id=None):
        try:
            if client_id:
                if paymode not in self.supported_paymodes:
                    raise RuntimeError("Paymode is not supported by the Payment Gateway")
                client = self.client_repository.get(client_id)
                client.add_paymode(paymode)
            else:
                self.supported_paymodes.add(paymode)
        except Exception as err:
            raise err
    
    def remove_paymode_support(self, paymode, client_id=None):
        try:
            if client_id:
                client = self.client_repository.get(client_id)
                if paymode not in client.get_supported_paymodes():
                    raise RuntimeError("Paymode is not supported by the provided client")
                client.remove_paymode(paymode)
            else:
                self.supported_paymodes.remove(paymode)
                clients = self.client_repository.list()
                for client in clients:
                    if paymode in client.get_supported_paymodes():
                        client.remove_paymode(paymode)
        except Exception as err:
            raise err
    
    def make_payment(self, payment_request):
        try:
            client_id = payment_request.client_id
            client = self.client_repository.get(client_id)
            
            if not client.validate_paymode_support(payment_request.paymode):
                raise ValueError("Invalid paymode for this client")
            
            payment_instrument = payment_request.instrument
            if payment_request.paymode != payment_instrument.get_paymode():
                raise ValueError("Payment request contains contradicting paymode and payment instrument")
            
            if not payment_instrument.validate():
                raise ValueError("Payment details missing for this payment instrument")
            
            bank = self.router.choose_bank(payment_request)
            val = bank.process_payment()
            if val == 0:
                return "FAILURE"
            return "SUCCESS"
        
        except Exception as err:
            raise err
        

if __name__ == '__main__':
    paymentGateway = PaymentGateway(supported_paymodes=[Paymode.UPI, Paymode.CARD])
    c1 = paymentGateway.add_client("C1", "Flipkart", [Paymode.CARD])
    c2 = paymentGateway.add_client("C2", "Amazon", [])
    c3 = paymentGateway.add_client("C3", "Myntra", [Paymode.UPI])
    b1 = Bank("HDFC")
    b2 = Bank("AXIS")
    b3 = Bank("ICICI")

    print(paymentGateway.list_supported_paymodes())
    print("-"*20)

    print(paymentGateway.has_client("C1"))
    print(paymentGateway.has_client("C2"))
    print(paymentGateway.has_client("C3"))
    print("-"*20)

    paymentGateway.remove_client("C3")
    print(paymentGateway.has_client("C1"))
    print(paymentGateway.has_client("C2"))
    print(paymentGateway.has_client("C3"))
    print("-"*20)

    print(paymentGateway.list_supported_paymodes("C1"))
    print(paymentGateway.list_supported_paymodes("C2"))
    paymentGateway.add_paymode_support(Paymode.NETBANKING)
    paymentGateway.add_paymode_support(Paymode.UPI, "C1")
    paymentGateway.add_paymode_support(Paymode.NETBANKING, "C1")
    print(paymentGateway.list_supported_paymodes("C1"))
    paymentGateway.add_paymode_support(Paymode.UPI, "C2")
    paymentGateway.add_paymode_support(Paymode.CARD, "C2")
    paymentGateway.add_paymode_support(Paymode.NETBANKING, "C2")
    print(paymentGateway.list_supported_paymodes("C2"))
    paymentGateway.remove_paymode_support(Paymode.NETBANKING, "C2")
    print(paymentGateway.list_supported_paymodes("C2"))
    print("-"*20)

    
    paymentGateway.router.register_strategy(Paymode.UPI, MappingRoutingStrategy({Paymode.UPI: b1}))
    paymentGateway.router.register_strategy(Paymode.CARD, MappingRoutingStrategy({Paymode.CARD: b2}))
    paymentGateway.router.register_strategy(Paymode.NETBANKING, WeightedRoutingStrategy([b1, b2, b3], [50, 25, 25]))

    payment_request1 = PaymentRequest("C1", 50, Paymode.UPI, UPIInstrument({
        "vpa": "hello@okhdfcbank"
    }))
    print(paymentGateway.make_payment(payment_request1))
    payment_request2 = PaymentRequest("C1", 40, Paymode.NETBANKING, NetbankingInstrument({
        "username": "hello",
        "password": "world"
    }))
    print(paymentGateway.make_payment(payment_request2))
    payment_request3 = PaymentRequest("C2", 40, Paymode.CARD, CardInstrument({
        "card_number": "123",
        "expiry": "03/26",
        "cvv": 111
    }))
    print(paymentGateway.make_payment(payment_request3))
    print("-"*20)

