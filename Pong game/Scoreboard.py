import pygame

class ScoreBoard:
    def __init__(self):
        # Player 1 score (left paddle)
        self.p1_score = 0
        
        # Player 2 score (right paddle / AI)
        self.p2_score = 0
        
        # Create a font object used to draw text on screen
        # The default pygame font is none and the 74 is the font size 
        
        self.font = pygame.font.Font(None, 74)


    def score_left(self):
        # Keeps track of when the left side (paddle) scores
        # Just adds one to the score variable
        self.p1_score += 1


    def score_right(self):
        # Keeps track of when the right side (paddle) scores
        # Just adds one to the score variable        
        self.p2_score += 1


    def render(self, screen, screen_width):
        # Convert the score numbers into text images that pygame can draw
        
        # Create text surface for player 1 score
        # str() converts the number to text
        # True = anti-aliasing (smooth text, never knew what this did till now)
        # (255,255,255) is the white color used
        left_text = self.font.render(str(self.p1_score), True, (255,255,255))

        # Create text surface for player 2 score
        # Same reasoning as before
        right_text = self.font.render(str(self.p2_score), True, (255,255,255))


        # Draws the text surfaces onto the screen
        # Bilt just copies images onto the screen
        
        # Left score position (left side of screen)
        screen.blit(left_text, (screen_width//4, 20))

        # Right score position (right side of screen)
        screen.blit(right_text, (screen_width*3//4, 20))