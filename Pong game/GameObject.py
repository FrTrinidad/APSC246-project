from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def render(self, screen):
        pass