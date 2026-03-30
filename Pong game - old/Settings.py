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
            self.difficulty_names = ["EASY", "MEDIUM", "HARD"]
            self.target_score = 5 # The target score
            self.bg_speed = 0 # Background speed

            # The background flashing speed control
            self.bg_speed_names = ["NONE", "SLOW", "MEDIUM", "FAST"]

            # I am not gonna go around and reprogam the background stuff
            # So the none is just so large it will practically never happen
            # I mean, if we're counting its 53 years. Have fun playing that long
            self.bg_speed_values = [100000000000, 60, 30, 15] 

            # Alright, new idea for difficulty
            # We are now changing three variables to account for it
            # The difficulty settings are now ball_speed, paddle_height, ai_speed
            # The player speed is always 5 - AI speed so that you can outrun it
            self.difficulty_settings = {
                "EASY":   {"ball_speed": 7, "paddle_height": 80, "ai_speed": 2.5, "reaction_zone": 0.65},
                "MEDIUM": {"ball_speed": 8, "paddle_height": 60, "ai_speed": 3.5, "reaction_zone": 0.50},
                "HARD":   {"ball_speed": 9, "paddle_height": 45, "ai_speed": 4.5, "reaction_zone": 0.30},
            }
        

            # Menu options for this screen
            self.menu_options = ["VOLUME", "DIFFICULTY", "TARGET SCORE", "BACKGROUND SPEED", "BACK"]
            
            # Small font for values
            self.value_font = pygame.font.Font("Fonts/aa.ttf", 14)

    def navigate(self, direction):
            #Movement between settings options
            super().navigate(direction)
        
    def adjust(self, direction):
        # Used to adjust the currently selected setting.
        # direction are -1 for decrease and 1 for increase

        # Gets the currently selected option from the menu 
        current_option = self.menu_options[self.selected_index]
        
        # If the option is volume
        if current_option == "VOLUME":
            # Increase/decrease volume in by 10
            self.volume += direction * 10

            # Sets max and min volume (Stays between 0 - 100)
            self.volume = max(0, min(100, self.volume))  
        
        # If the option is difficulty
        elif current_option == "DIFFICULTY":
            # Increases the difficulty index (See above)
            self.difficulty += direction
            
            # Sets max and min (Stays between 0 - 2)
            self.difficulty = max(0, min(2, self.difficulty))  # Clamp 0-2

        # If its target score
        # Changes the target score for match
        elif current_option == "TARGET SCORE":
            self.target_score += direction
            self.target_score = max(1, min(15, self.target_score))  # 1-15 range
        # If its background speed
        # Changes the backgrounf flashing speed
        elif current_option == "BACKGROUND SPEED":
            self.bg_speed += direction
            self.bg_speed = max(0, min(3, self.bg_speed))  # 1-4 range


    
    def get_difficulty_settings(self):
        # Returns the difficulty settings as a dict
        name = self.difficulty_names[self.difficulty]
        return self.difficulty_settings[name]
    
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
            if option == "VOLUME":
                # Shows the volume value with the arrows around it
                display_text = f"{indicator}VOLUME: < {self.volume}% >"
            elif option == "DIFFICULTY":
                # Displays the difficulty name 
                display_text = f"{indicator}DIFFICULTY: < {self.difficulty_names[self.difficulty]} >"
            elif option == "TARGET SCORE":
                # Display target score
                display_text = f"{indicator}TARGET SCORE: < {self.target_score} >"
                #Display Background speed
            elif option == "BACKGROUND SPEED":
                display_text = f"{indicator}BG SPEED: < {self.bg_speed_names[self.bg_speed]} >"
            else:
                # The default case for the option without all the extra values
                display_text = f"{indicator}{option}"
            
            text_surf = self.font.render(display_text, True, color)
            rect = text_surf.get_rect(center=(screen_width // 2, start_y + i * 70))
            screen.blit(text_surf, rect)
        
        # Instructions at the bottom of the screen
        instructions = "UP/DOWN: NAVIGATE | LEFT/RIGHT: ADJUST | ENTER: SELECT"

        # Renders the instructions
        inst_surf = self.value_font.render(instructions, True, (80, 80, 80))

        # Positions them
        inst_rect = inst_surf.get_rect(center=(screen_width // 2, screen_height - 50))

        # Draws it
        screen.blit(inst_surf, inst_rect)
        
        #Updates the display to everything that is drawn
        pygame.display.flip()