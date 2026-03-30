import pygame
from UI import UI

class EndScreen(UI):
    # The end screen displayed when a player wins.
    # Shows the winner and options to play again or quit.
    
    
    def __init__(self):
        super().__init__()

        # Current screen type
        self.current_screen = "END"

        # Menu options on the screen
        self.menu_options = ["PLAY AGAIN", "MAIN MENU", "QUIT"]

        # Winner info, initially none
        self.winner = None  # "Player 1", "Player 2", or "AI"

        # Final scores
        self.final_score = (0, 0)  # (p1_score, p2_score)
        
        # Fonts for the differnent texts
        self.winner_font = pygame.font.Font("Fonts/aa.ttf", 80)
        self.score_font = pygame.font.Font("Fonts/aa.ttf", 50)
    
    def set_winner(self, winner, p1_score, p2_score):
        # Set the winner information to display.
        
        # Saves the winner name
        self.winner = winner

        # Saves the final score as a tuple
        self.final_score = (p1_score, p2_score)
    
    def select(self):
        # Return the selected menu option
        return self.menu_options[self.selected_index]
    
    def render(self, screen, screen_width, screen_height):        
        # Winner announcement text
        if self.winner:
            # Creates the winner anouncement text
            winner_text = f"{self.winner} WINS!"
            
            # Renders it as a surface in gold
            winner_surf = self.winner_font.render(winner_text, True, (255, 215, 0))  

            #Centers it close to the top of the screen
            winner_rect = winner_surf.get_rect(center=(screen_width // 2, 100))

            # Draws it onto the screen
            screen.blit(winner_surf, winner_rect)
        
        # Final score

        # Same general process as before
        score_text = f"FINAL SCORE: {self.final_score[0]} - {self.final_score[1]}"
        # This is white though not gold
        score_surf = self.score_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(screen_width // 2, 180))
        screen.blit(score_surf, score_rect)
        
        # Divider line
        # Draws a horizontal line to seperate the scores from the menu 
        pygame.draw.line(screen, (100, 100, 100), 
                         (screen_width // 4, 230), 
                         (3 * screen_width // 4, 230), 2)
        
        # Menu options
        
        # Starting Y position for the menu items
        start_y = screen_height // 2 + 20

        # Loops through each option
        for i, option in enumerate(self.menu_options):

            # Highlights the selected option 
            if i == self.selected_index:
                color = (255, 255, 255) # White
                prefix = "> " # Indicator
            else:
                color = (100, 100, 100) # Grey
                prefix = "  " # No indicator
            
            text_surf = self.font.render(prefix + option, True, color)
            rect = text_surf.get_rect(center=(screen_width // 2, start_y + i * 60))
            screen.blit(text_surf, rect)
        
        pygame.display.flip()