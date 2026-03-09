from abc import ABC, abstractmethod
from PaymentInstrument import Paymode
import random

class RoutingStrategy(ABC):
    @abstractmethod
    def route(self, request):
        pass

class MappingRoutingStrategy(RoutingStrategy):
    def __init__(self, instrument_mapping):
        self.instrument_mapping = instrument_mapping
    
    def route(self, request):
        if request.paymode not in self.instrument_mapping:
            raise KeyError("Paymode not supported by PG")
        bank = self.instrument_mapping[request.paymode]
        return bank
    
class WeightedRoutingStrategy(RoutingStrategy):
    def __init__(self, banks, weights):
        self.banks = banks
        self.weights = weights
        
    def route(self, request):
        bank = random.choices(self.banks, self.weights, k=1)        
        return bank[0]