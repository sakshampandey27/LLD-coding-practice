from abc import ABC, abstractmethod

class EvictionStrategy(ABC):
    @abstractmethod
    def get(self, key):
        pass
    
    @abstractmethod
    def put(self, key, value):
        pass
