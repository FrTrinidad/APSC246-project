import pygame

class InputHandler:
    
    # Handles all input reading and translates them into game actions.
    # Currently keyboard-only. I'll deal with GPIO support later/when testing on the Pi.
    
    
    # Action constants
    ACTION_UP = "up"
    ACTION_DOWN = "down"
    ACTION_LEFT = "left"
    ACTION_RIGHT = "right"
    ACTION_CONFIRM = "confirm"
    ACTION_BACK = "back"
    ACTION_START = "start"
    ACTION_QUIT = "quit"
    ACTION_VOLUME_UP = "volume_up"
    ACTION_VOLUME_DOWN = "volume_down"
    
    def __init__(self):
        # Key mappings
        self.key_mappings = {
            pygame.K_UP: self.ACTION_UP,
            pygame.K_DOWN: self.ACTION_DOWN,
            pygame.K_LEFT: self.ACTION_LEFT,
            pygame.K_RIGHT: self.ACTION_RIGHT,
            pygame.K_RETURN: self.ACTION_CONFIRM,
            pygame.K_ESCAPE: self.ACTION_BACK,
            pygame.K_SPACE: self.ACTION_START,
            pygame.K_EQUALS: self.ACTION_VOLUME_UP,   # + key
            pygame.K_MINUS: self.ACTION_VOLUME_DOWN,
        }
        
        # Alternative mappings for WASD controls
        self.alt_mappings = {
            pygame.K_w: self.ACTION_UP,
            pygame.K_s: self.ACTION_DOWN,
            pygame.K_a: self.ACTION_LEFT,
            pygame.K_d: self.ACTION_RIGHT,
        }
        
        # Stores the actions that are being held down
        self.pressed_actions = set()

        # Stores the actions pressed during the current frame
        self.just_pressed = set()

        # Keeps track on whether or not the player wants to quit 
        self.quit_requested = False
    
    def poll(self):
        # Call once per frame to update input states

        # Clears the last frame's "just pressed" action
        self.just_pressed.clear()
        
        # Loops through the availabe pygame events 
        for event in pygame.event.get():

            # If the user clicks the window close button
            if event.type == pygame.QUIT:
                self.quit_requested = True
            
            # If a key is pressed down
            elif event.type == pygame.KEYDOWN:

                # Converst the key into a action depending on the mappings
                action = self.key_mappings.get(event.key) or self.alt_mappings.get(event.key)

                # If its mapped to something
                if action:
                    # Marks it as held
                    self.pressed_actions.add(action)

                    #Marks it as pressed this frame
                    self.just_pressed.add(action)
            
            # When the key is released
            elif event.type == pygame.KEYUP:

                # Convers it into a action
                action = self.key_mappings.get(event.key) or self.alt_mappings.get(event.key)

                # Removes it from the held actions
                if action:
                    self.pressed_actions.discard(action)
        
        # Returns the list of actions that were pressed during the frame
        return list(self.just_pressed)
    
    def is_pressed(self, action):
        # Check if action is held down (continuous movement)
        return action in self.pressed_actions
    
    def is_just_pressed(self, action):
        # Check if action was just pressed this frame (for menu navigation)
        return action in self.just_pressed
    
    def should_quit(self):
        # If the user wants to quite
        return self.quit_requested
    
    def cleanup(self):
        # Ignore this for now, its just a placeholder for future GPIO stuff
        pass