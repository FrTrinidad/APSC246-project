import pygame

class ScoreBoard:
    def __init__(self):
        # Player 1 score (left paddle)
        self.p1_score = 0
        
        # Player 2 score (right paddle / AI)
        self.p2_score = 0
        
        # Create a font object used to draw text on screen
        self.font = pygame.font.Font("fonts/aa.TTF", 74)


    def score_left(self):
        # Keeps track of when the left side (paddle) scores
        # Just adds one to the score variable
        self.p1_score += 1


    def score_right(self):
        # Keeps track of when the right side (paddle) scores
        # Just adds one to the score variable        
        self.p2_score += 1


    def render(self, screen, screen_width, target_score):
        # Convert the score numbers into text images that pygame can draw
        
        # Displays the winning score
        label_font = pygame.font.Font("Fonts/aa.TTF", 33)
        target_text = label_font.render(f"FIRST TO {target_score}", True, (0, 0, 0))

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
        screen.blit(left_text, (screen_width//4, 50))

        # Right score position (right side of screen)
        screen.blit(right_text, (screen_width*3//4, 50))

        # First to score X (Middle of the screen)
        screen.blit(target_text, (screen_width // 2 - target_text.get_width() // 2, 10))
