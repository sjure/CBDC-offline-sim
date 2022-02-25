from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self, method):
        self.method = method
    
    @abstractmethod
    def execute(self):
        self.method()