from abc import ABC, abstractmethod
class Node(ABC):    
    def __init__(self):
        pass
    
    @abstractmethod
    def tick(self):
        pass
