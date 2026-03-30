import pygame
from UI import UI

class Menu(UI):  
    def __init__(self, options):
        super().__init__()
        self.menu_options = options           # list of menu items
        self.selected_index = 0          # which option is currently highlighted
        self.pong_font = pygame.font.Font("fonts/aa.TTF", 115)  # Extra big just for PONG title
    
    def select(self):
        # Returns the selected option string
        return self.menu_options[self.selected_index]  # <-- Fixed
    
    def render(self, screen, screen_width, screen_height):

    # Title at top
        title_surf = self.pong_font.render("[ PONG GAME ]", True, (255, 255, 255)) 
        title_rect = title_surf.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_surf, title_rect)

    # Would have been nice to know earlier
    # Enumerate just loops over a list and gets both index and the item
    # Text in pygame requires a surface, text_surf reads from that box
        for i, option in enumerate(self.menu_options):  
            if i == self.selected_index: 
                color = (255,255,255) 
            else:
                color = (100,100,100)
            text_surf = self.font.render(option, True, color)
            rect = text_surf.get_rect(center=(screen_width//2, screen_height//2 + i*60))
            screen.blit(text_surf, rect)
        
        pygame.display.flip()