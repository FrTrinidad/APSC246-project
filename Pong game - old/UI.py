import pygame
from abc import ABC, abstractmethod

class UI(ABC):
    #This is the base class for all UI screens
    #So things like menus, settings, screens, etc
    #It deals with basic functionality like rendering backgounds and navigation 
    def __init__(self):
        # Track what's being displayed
        self.current_screen = None  
        # Available options for this screen
        self.menu_options = []      
        # Currently highlighted option       
        self.selected_index = 0           
        self.font = pygame.font.Font("Fonts/aa.ttf", 50)
        self.title_font = pygame.font.Font("Fonts/aa.ttf", 70)

    @abstractmethod
    def render(self, screen, screen_width, screen_height):
        pass

    def navigate(self, direction):
        # Handle movement between options.
        # Direction is -1 for up, 1 for down

        self.selected_index += direction
        # Wrap around if we go over the bounds
        if self.selected_index < 0:
            self.selected_index = len(self.menu_options) - 1
        elif self.selected_index >= len(self.menu_options):
            self.selected_index = 0
    
    def select(self):
        # Confirm the current selection
        # Also returns the selected option
        if self.menu_options:
            return self.menu_options[self.selected_index]
        return None
    
    def render_title(self, screen, title, screen_width, y_pos=80):
        # Helps to render a title at the top of the screen
        # title_surf is the surface so that the image of the rendered text an be drawn
        # title_rect is the position and size box that tells pygame where and how to place the text image on the screen
        title_surf = self.title_font.render(title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen_width // 2, y_pos))
        screen.blit(title_surf, title_rect)

    def render_options(self, screen, screen_width, screen_height, start_y=None):
        # Helper to render menu options with some nice highlighting

        # If we arent given a starting y position, it calcualtes one roughly in the center of the menu (vertically)
        if start_y is None:
            start_y = screen_height // 2 - (len(self.menu_options) * 30)
        
        # Loops through the menu options
        for i, option in enumerate(self.menu_options):

            # Checks if this option is the currently selected one
            if i == self.selected_index:
                color = (255, 255, 255)  # White for selected
            else:
                color = (100, 100, 100)  # Gray for unselected
            
            # Converts the text given into a drawable image (surface)
            text_surf = self.font.render(option, True, color)

            # Creates the rectangle so that we can position the text
            rect = text_surf.get_rect(center=(screen_width // 2, start_y + i * 60))
           
            # Draws the text onto the screen
            screen.blit(text_surf, rect)