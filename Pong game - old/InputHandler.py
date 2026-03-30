import pygame

try:
    from gpiozero import Button
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

class InputHandler:
    
    # Handles all input reading and translates them into game actions.    
    
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

        self.gpio_buttons = []

        if GPIO_AVAILABLE:
            self.setup_gpio()

    def setup_gpio(self):
        # Your pin mappings

        # We are using a 2D list here since we wanna keep duplicates
        pin_mappings = [
            # Buttons
            (22, self.ACTION_UP),
            (26, self.ACTION_DOWN),
            (5, self.ACTION_LEFT),
            (6, self.ACTION_RIGHT),
            (27, self.ACTION_BACK),
            (17, self.ACTION_QUIT),
            (24, self.ACTION_VOLUME_UP),
            (25, self.ACTION_VOLUME_DOWN),
            (3, self.ACTION_CONFIRM),
            # Joystick
            (2, self.ACTION_UP),
            (4, self.ACTION_DOWN),
            (15, self.ACTION_LEFT),
            (18, self.ACTION_RIGHT),
        ]
        
        # Loops through each GPIO pin and their actions
        for pin, action in pin_mappings:
            try:
                # Creates a button object for the given GPIO pin
                # pull_up = true just emans that pin is usually high and low when pressed
                # bounce time makes sure we dont get multiple triggers from the same press
                btn = Button(pin, pull_up=True, bounce_time=0.05)

                # Stores the button object in a dict using the action as the key
                # So we can now easily check which button corresponds to what game action
                self.gpio_buttons.append((action, btn))
            except Exception as e:
                # If theres some error when setting up the pins (so invalid or hardware issues)
                # Prints a error message
                print(f"Could not setup GPIO pin {pin}: {e}")
        
    
    def poll(self):
        # Call once per frame to update input states

        # Clears the last frame's "just pressed" action
        self.just_pressed.clear()
        
        # KEYBOARD EVENTS

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


        # GPIO BUTTON EVENTS (Has to be on PI)

        # Only checks if the GPIO stuff is availabe
        if GPIO_AVAILABLE:

            # Loops through all mapped actions and their button objects
            for action, btn in self.gpio_buttons:

                # Checks if a button is being pressed
                if btn.is_pressed:

                    # If it wasnt pressed in the last frame
                    # So it was pressed this frame
                    if action not in self.pressed_actions:
                        self.just_pressed.add(action)   # Tracks the new presses
                    
                    # Adds the action to the set of currently pressed actions
                    self.pressed_actions.add(action)
                else:
                    # If the button is not pressed we remove it from the pressed set
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
        if GPIO_AVAILABLE:
            # Loops through all the button objects that are stored
            for action, btn in self.gpio_buttons:
                # Closes the button
                # Just means that we are releasing the GPIO pin and cleaning up resources
                # Used when restarting the program/reinitializing GPIO
                btn.close()