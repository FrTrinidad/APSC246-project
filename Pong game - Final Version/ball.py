import pygame
import random
from GameObject import GameObject

class Ball(GameObject):
    def __init__(self, x, y, radius=10):
        super().__init__(x, y)
        self.radius = radius
        self.base_speed = 5  # The default speed
        self.x_velocity = self.base_speed
        self.y_velocity = self.base_speed
        self.moving = False
        self.trail = []      # Will store the previous positions 

        # Randomizes the initial direction 
        self.randomize_direction()
    
    def randomize_direction(self):
        # Random X direction (left or right)
        self.x_velocity = random.choice([-1, 1]) * abs(self.x_velocity)
        
        # Random Y direction with (includes some angle variation)
        self.y_velocity = random.choice([-1, 1]) * abs(self.y_velocity)
        # Add slight variation so it's not always 45 degrees
        self.y_velocity *= random.uniform(0.5, 1.0)

    def set_speed(self, speed):
        # Keeps direction while changing magnitude
        x_dir = 1 if self.x_velocity >= 0 else -1
        y_dir = 1 if self.y_velocity >= 0 else -1
        self.x_velocity = speed * x_dir
        self.y_velocity = speed * y_dir * random.uniform(0.5, 1.0)

    def update(self):
        if self.moving:  # Only move if started

            self.trail.append((self.x, self.y))
            if len(self.trail) > 8:  # Keep last 8 positions
                self.trail.pop(0)

            self.x += self.x_velocity
            self.y += self.y_velocity
    
    def render(self, screen):

        # Draw trail (fading circles)
        for i, pos in enumerate(self.trail):
            # Calculates the brightness, the older ones are darker and newer ones are lighter
            # i is going from 0 (the newest) to len(trail - 1) (newest)
            brightness = int(30 + (70 * i / len(self.trail))) if self.trail else 0

            # Calculates the circle sizes
            # The older ones are smaller, newer ones are bigger
            trail_radius = int(self.radius * (0.3 + (0.5 * i / len(self.trail)))) if self.trail else 0

            # Draws the circle at the position=
            pygame.draw.circle(screen, (brightness, brightness, brightness), 
                              (int(pos[0]), int(pos[1])), trail_radius)

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

        # Clears the trail on a reset 
        self.trail.clear()

        # New randomized direction
        self.randomize_direction()
