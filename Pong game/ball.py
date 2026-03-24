import pygame
from GameObject import GameObject

class Ball(GameObject):
    def __init__(self, x, y, radius=10):
        super().__init__(x, y)
        self.radius = radius
        self.base_speed = 5  # The default speed
        self.x_velocity = self.base_speed
        self.y_velocity = self.base_speed
        self.moving = False
    
    def set_speed(self, speed):
        # Keeps direction, changes magnitude
        self.x_velocity = speed if self.x_velocity >= 0 else -speed
        self.y_velocity = speed if self.y_velocity >= 0 else -speed
    
    def update(self):
        if self.moving:  # Only move if started
            self.x += self.x_velocity
            self.y += self.y_velocity
    
    def render(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)
    
    def bounce_x(self):
        self.x_velocity = -self.x_velocity
    
    def bounce_y(self):
        self.y_velocity = -self.y_velocity
    
    def start(self):
        self.moving = True
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.moving = False  # Stop on reset