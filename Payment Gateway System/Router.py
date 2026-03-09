class Router:
    def __init__(self):
        self.routing_strategies = {}
    
    def register_strategy(self, paymode, strategy):
        self.routing_strategies[paymode] = strategy

    def choose_bank(self, payment_request):
        strategy = self.routing_strategies.get(payment_request.paymode, None)
        if not strategy:
            raise RuntimeError("No routing strategy configured for this paymode")
        return strategy.route(payment_request)