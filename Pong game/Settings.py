import pygame
from UI import UI

# Is the setting screen that handles the configuration for game controls
# Handles thinsg like volume, difficulty, and other configurable options 

class Settings(UI):

    def __init__(self):
            super().__init__()
            self.current_screen = "settings"
            
            # Configurable options, gives the default values too
            self.volume = 50          # 0-100
            self.difficulty = 1       # 0 = Easy, 1 = Medium, 2 = Hard
            self.difficulty_names = ["Easy", "Medium", "Hard"]
            self.difficulty_speeds = [3, 5, 7]  # Ball Speeds
            
            # Menu options for this screen
            self.menu_options = ["Volume", "Difficulty", "Back"]
            
            # Small font for values
            self.value_font = pygame.font.SysFont("Arial", 40)

    def navigate(self, direction):
            #Movement between settings options
            super().navigate(direction)
        
    def adjust(self, direction):
        # Used to adjust the currently selected setting.
        # direction are -1 for decrease and 1 for increase

        # Gets the currently selected option from the menu 
        current_option = self.menu_options[self.selected_index]
        
        # If the option is volume
        if current_option == "Volume":
            # Increase/decrease volume in by 10
            self.volume += direction * 10

            # Sets max and min volume (Stays between 0 - 100)
            self.volume = max(0, min(100, self.volume))  
        
        # If the option is difficulty
        elif current_option == "Difficulty":
            # Increases the difficulty index (See above)
            self.difficulty += direction
            
            # Sets max and min (Stays between 0 - 2)
            self.difficulty = max(0, min(2, self.difficulty))  # Clamp 0-2
    
    def get_ball_speed(self):
        # Returns the ball speed based on the current difficulty
        return self.difficulty_speeds[self.difficulty]

    def get_volume(self):
        # Returns volume as a float (0.0-1.0) so that we can use it in the pygame mixer
        return self.volume / 100.0
    
    def save(self):
        # Store preferences (This is a placeholder for future file-based saving, might change).
        # As it is now, it returns current settings as a dict.
        
        return {
            "volume": self.volume,
            "difficulty": self.difficulty
        }
    
    def load(self, settings_dict):
        # Load settings from the dictionary
        if "volume" in settings_dict:
            self.volume = settings_dict["volume"]
        if "difficulty" in settings_dict:
            self.difficulty = settings_dict["difficulty"]
    
    def select(self):
        # Returns the selected option (used later for the Back button)
        return self.menu_options[self.selected_index]
    
    def render(self, screen, screen_width, screen_height):
        # Renders the settings screen
        
         # Black background
        screen.fill((0, 0, 0))

        # Draws the ttile at the top
        self.render_title(screen, "SETTINGS", screen_width, 80)
        
        # Render each setting with its current value
        start_y = screen_height // 2 - 60
        
        # Loops through each of the menu options
        for i, option in enumerate(self.menu_options):

            # Does the color and indicator depending on selection
            if i == self.selected_index:
                # White if selected
                color = (255, 255, 255)

                # Arrow to show selection
                indicator = "> "
            else:
                # Gray if not selected
                color = (100, 100, 100)

                # No indicator
                indicator = "  "
            
            # Get the display text based on option type
            if option == "Volume":
                # Shows the volume value with the arrows around it
                display_text = f"{indicator}Volume: < {self.volume}% >"
            elif option == "Difficulty":
                # Displays the difficulty name 
                display_text = f"{indicator}Difficulty: < {self.difficulty_names[self.difficulty]} >"
            else:
                # The default case for the option without all the extra values
                display_text = f"{indicator}{option}"
            
            text_surf = self.font.render(display_text, True, color)
            rect = text_surf.get_rect(center=(screen_width // 2, start_y + i * 70))
            screen.blit(text_surf, rect)
        
        # Instructions at the bottom of the screen
        instructions = "UP/DOWN: Navigate | LEFT/RIGHT: Adjust | ENTER: Select"

        # Renders the instructions
        inst_surf = self.value_font.render(instructions, True, (80, 80, 80))

        # Positions them
        inst_rect = inst_surf.get_rect(center=(screen_width // 2, screen_height - 50))

        # Draws it
        screen.blit(inst_surf, inst_rect)
        
        #Updates the display to everything that is drawn
        pygame.display.flip()