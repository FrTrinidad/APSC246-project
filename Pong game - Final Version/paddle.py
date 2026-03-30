import pygame
from GameObject import GameObject

class Paddle(GameObject):
    def __init__(self, x, y, screen_height, width=10, height=60):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.speed = 5
        self.screen_height = screen_height
    
    
    def update(self):
        pass  # Movement handled by move_up/move_down
    
    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
    
    def move_up(self):
        if self.y > 0:
            self.y -= self.speed
    
    def move_down(self):
        if self.y + self.height < self.screen_height:
            self.y += self.speed
    
    def get_bounds(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)