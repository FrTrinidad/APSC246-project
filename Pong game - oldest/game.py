import pygame
from ball import Ball
from paddle import Paddle
from AIController import AIController
from Scoreboard import ScoreBoard
from menu_class import Menu
from Settings import Settings         
from EndScreen import EndScreen        
from InputHandler import InputHandler  

class Game:

    # Game states
    STATE_MENU = "menu"
    STATE_SETTINGS = "settings"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_END = "end"

    # The win condition
    WINNING_SCORE = 5
    

    def __init__(self):
        pygame.init()
        
        # Screen dimensions --> keep in mind this is not resolution, pixels are fixed and dont adapt to physical screen size
        self.screen_width = 800
        self.screen_height = 600
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        # Game state (replaces self.in_menu)
        self.state = self.STATE_MENU
        
        # Initialize input handler
        self.input_handler = InputHandler()
                
        # Create objects using screen dimensions
        self.ball = Ball(self.screen_width // 2, self.screen_height // 2)
        self.paddle1 = Paddle(50, self.screen_height // 2 - 30, self.screen_height)
        self.paddle2 = Paddle(self.screen_width - 60, self.screen_height // 2 - 30, self.screen_height)
       
        # Initialize the AI
        self.ai = AIController(self.ball, self.paddle2)

        # Initialize the Scoreboard
        self.scoreboard = ScoreBoard()  # Note: lowercase now

        # UI Screens
        self.menu = Menu(["Start Game", "Settings", "Quit"])
        self.settings = Settings()
        self.end_screen = EndScreen()
        
        # Apply initial settings
        self._apply_settings()

    def _apply_settings(self):
        # Applies the current settings to game objects
        # Set ball speed based on difficulty
        self.ball.set_speed(self.settings.get_ball_speed())

    def handle_menu_events(self):
        """Handle input in main menu"""
        self.input_handler.poll()
        
        if self.input_handler.should_quit():
            self.is_running = False
            return
        
        # Moves up in the menu if up the up arrow is pressed
        if self.input_handler.is_just_pressed(InputHandler.ACTION_UP):
            self.menu.navigate(-1)
        
        # Moves down in the menu if the down arrow is pressed
        if self.input_handler.is_just_pressed(InputHandler.ACTION_DOWN):
            self.menu.navigate(1)
        
        # Selects the option if enter/return is pressed
        if self.input_handler.is_just_pressed(InputHandler.ACTION_CONFIRM):
            choice = self.menu.select()
            
            # If "Start Game" is pressed the game loop starts
            if choice == "Start Game":
                self.reset_game()
                self.state = self.STATE_PLAYING
            # If "Settings" is pressed, go to settings
            elif choice == "Settings":
                self.state = self.STATE_SETTINGS
            # If "Quit" is pressed then the game stops 
            elif choice == "Quit":
                self.is_running = False
        
    def handle_settings_events(self):
        # Handles input in settings screen

        # Updates the input handler for the current frame (poll kboard, etc)
        self.input_handler.poll()
        
        # If the user wants to quit (so like closed window)
        if self.input_handler.should_quit():
            self.is_running = False
            return
        
        # Navigations stuff

        # Move up
        if self.input_handler.is_just_pressed(InputHandler.ACTION_UP):
            self.settings.navigate(-1)
        
        # Move down
        if self.input_handler.is_just_pressed(InputHandler.ACTION_DOWN):
            self.settings.navigate(1)
        
        # Adjusts the settings value

        # Decrease the setting value
        if self.input_handler.is_just_pressed(InputHandler.ACTION_LEFT):
            self.settings.adjust(-1) # Decreases it
            self._apply_settings() # Updates the game with the new settings
        
        # Increase the setting value
        if self.input_handler.is_just_pressed(InputHandler.ACTION_RIGHT):
            self.settings.adjust(1) # Increases it
            self._apply_settings() # Updates the game with the new settings
        
        # Confirms the selection
        if self.input_handler.is_just_pressed(InputHandler.ACTION_CONFIRM):
            choice = self.settings.select() # Gets the currently selected option
            if choice == "Back": # if back is selected
                self.state = self.STATE_MENU # Returns to the main menu
        
        # If back/escape is used
        if self.input_handler.is_just_pressed(InputHandler.ACTION_BACK):
            self.state = self.STATE_MENU # Back to main menu

    def handle_game_events(self):
        # Handles the input during gameplay

        # Update the input handler for this frame (poll keyboard, etc.)
        self.input_handler.poll()

        # Quits if requested        
        if self.input_handler.should_quit():
            self.is_running = False
            return
        
        # Press space to start
        if self.input_handler.is_just_pressed(InputHandler.ACTION_START):
            if not self.ball.moving:
                self.ball.start() # starts ball movement
        
        # Press escape to go back to menu
        if self.input_handler.is_just_pressed(InputHandler.ACTION_BACK):
            self.state = self.STATE_MENU
        
        # Gets the pressed keys (inputs) for paddle movement

        # Moves up if the up key is held down
        if self.input_handler.is_pressed(InputHandler.ACTION_UP):
            self.paddle1.move_up()

        # Moves down if the down key is held down
        if self.input_handler.is_pressed(InputHandler.ACTION_DOWN):
            self.paddle1.move_down()
    
    def handle_end_events(self):
        # Handles the input on the end screen
        
        # Update input states for this frame
        self.input_handler.poll()

        # Quits if requested
        if self.input_handler.should_quit():
            self.is_running = False
            return
        
        # Navigation

        # Move up
        if self.input_handler.is_just_pressed(InputHandler.ACTION_UP):
            self.end_screen.navigate(-1) # Move highlight up
        
        # Move down
        if self.input_handler.is_just_pressed(InputHandler.ACTION_DOWN):
            self.end_screen.navigate(1) # Move highlight down
        
        # Confirms selection
        if self.input_handler.is_just_pressed(InputHandler.ACTION_CONFIRM):
            #Gets the selected menu option
            choice = self.end_screen.select()
            
            # Performs a action depending on the choice
            if choice == "Play Again":
                self.reset_game() # Resets the game state
                self.state = self.STATE_PLAYING # Back to the game
            elif choice == "Main Menu":
                self.reset_game() # Resets the game state
                self.state = self.STATE_MENU # Back to main menu
            elif choice == "Quit":
                self.is_running = False # Quits game 


    def update(self):
        self.ball.update()
        self.ai.update()
        
        # Ball collision with top/bottom walls
        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = self.ball.radius
            self.ball.bounce_y()
        elif self.ball.y + self.ball.radius >= self.screen_height:
            self.ball.y = self.screen_height - self.ball.radius
            self.ball.bounce_y()
        
        # Ball collision with paddles
        ball_rect = pygame.Rect(
            self.ball.x - self.ball.radius, 
            self.ball.y - self.ball.radius, 
            self.ball.radius * 2, 
            self.ball.radius * 2
        )
        
        # Player paddle collision
        if ball_rect.colliderect(self.paddle1.get_bounds()) and self.ball.x_velocity < 0:
            self.ball.x = self.paddle1.x + self.paddle1.width + self.ball.radius
            self.ball.bounce_x()
        
        # AI paddle collision
        if ball_rect.colliderect(self.paddle2.get_bounds()) and self.ball.x_velocity > 0:
            self.ball.x = self.paddle2.x - self.ball.radius
            self.ball.bounce_x()
        
        # Ball out of bounds (score)
        # Updates the scoreboard too
        
        # If the ball goes off the LEFT side of the screen
        if self.ball.x <= 0:
            # Right player scores
            self.scoreboard.score_right()
            # Checks for win
            self._check_win_condition()
            # Only reset if game not over
            if self.state == self.STATE_PLAYING:  
                self.ball.reset(self.screen_width//2, self.screen_height//2)


        # If the ball goes off the RIGHT side of the screen
        if self.ball.x >= self.screen_width:
            # Left player scores
            self.scoreboard.score_left()
            # Checks for win
            self._check_win_condition()
            # Reset ball to the center
            if self.state == self.STATE_PLAYING:
                self.ball.reset(self.screen_width//2, self.screen_height//2)   

    def _check_win_condition(self):
        # Checks if someone has won

        # Checks if player one has won
        if self.scoreboard.p1_score >= self.WINNING_SCORE:
            # Updates the end screen with the proper info 
            self.end_screen.set_winner("Player 1", 
                                       self.scoreboard.p1_score, 
                                       self.scoreboard.p2_score)
            # Switches game state to end scren
            self.state = self.STATE_END

        # Checks if player two (AI) has won
        elif self.scoreboard.p2_score >= self.WINNING_SCORE:
            # Updates the end screen with the proper info 
            self.end_screen.set_winner("AI", 
                                       self.scoreboard.p1_score, 
                                       self.scoreboard.p2_score)
            # Switches gamet to end screen
            self.state = self.STATE_END

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draws the scoreboard onto the screen
        self.scoreboard.render(self.screen, self.screen_width)
        
        #Draws the paddles and ball
        self.ball.render(self.screen)
        self.paddle1.render(self.screen)
        self.paddle2.render(self.screen)

        #New frame, updates display
        pygame.display.flip()
    
    def reset_game(self):
        #Reset the game state for a new game

        # Resets the ball position
        self.ball.reset(self.screen_width // 2, self.screen_height // 2)

        # Resets paddle positions
        self.paddle1.y = self.screen_height // 2 - 30
        self.paddle2.y = self.screen_height // 2 - 30

        # Resets scoreboard
        self.scoreboard.p1_score = 0
        self.scoreboard.p2_score = 0

        # Resets the end screen selection
        self.end_screen.selected_index = 0

    def run(self):
        # The main game loop
        try:
            # Keeps looping while the game is running
            while self.is_running:
                # Handle different game states

                # Main menu state
                if self.state == self.STATE_MENU:
                    self.handle_menu_events()
                    self.menu.render(self.screen, self.screen_width, self.screen_height)
                
                # Setting state
                elif self.state == self.STATE_SETTINGS:
                    self.handle_settings_events()
                    self.settings.render(self.screen, self.screen_width, self.screen_height)
                
                # Gameplay state
                elif self.state == self.STATE_PLAYING:
                    self.handle_game_events()
                    self.update()
                    self.render()
                
                # End screen state
                elif self.state == self.STATE_END:
                    self.handle_end_events()
                    self.end_screen.render(self.screen, self.screen_width, self.screen_height)

                # Sets the game to 60 FPS
                self.clock.tick(60)
        
        finally:
            # Cleanup 
            # Keeps runing even if the error occurs/game exits
            self.input_handler.cleanup()
            pygame.quit()

# Assuming all goes well, runs the game
if __name__ == "__main__":
    game = Game()
    game.run()