from abc import ABC, abstractmethod

class BaseStrategie(ABC) :
    
    def __init__(self, candles) :
        self._candles = candles
    
    @abstractmethod
    def signal(self):
        pass