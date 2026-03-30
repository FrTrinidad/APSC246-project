import pygame
from ball import Ball
from paddle import Paddle
from AIController import AIController
from Scoreboard import ScoreBoard
from menu_class import Menu
from Settings import Settings         
from EndScreen import EndScreen        
from InputHandler import InputHandler 
from SoundManager import SoundManager 
import random



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
        
        self.screen_height = 400
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("PONG")
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
        self.ai = AIController(self.ball, self.paddle2, self.screen_width)

        # Initialize the Scoreboard
        self.scoreboard = ScoreBoard()  

        # Initialize the sounds stuff and music
        self.sound_manager = SoundManager()
        self.sound_manager.play_music()
        self.win_music_timer = 0
        self.lose_music_timer = 0

        # UI Screens
        self.menu = Menu(["START GAME", "SETTINGS", "QUIT"])
        self.settings = Settings()
        self.end_screen = EndScreen()
        
        # Apply initial settings
        self.apply_settings()

        # For the animated background
        self.bg_colors = []
        self.bg_timer = 0
        self._generate_bg_colors()
        
        # For the countdown
        self.countdown = 0
        self.countdown_active = False
        self.countdown_font = pygame.font.Font("fonts/aa.TTF", 150)
        self.first_round = True

    def start_countdown(self):
        self.countdown = 180  # 3 seconds at 60fps
        self.countdown_active = True

    def apply_settings(self):
        # Get all difficulty settings
        settings = self.settings.get_difficulty_settings()
        
        # Apply ball speed
        self.ball.set_speed(settings["ball_speed"])
        
        # Apply paddle heights (both paddles same size)
        self.paddle1.height = settings["paddle_height"]
        self.paddle2.height = settings["paddle_height"]
        
        # Apply AI speed (slower than player)
        self.ai.speed = settings["ai_speed"]

        # Apply the reaction zone
        self.ai.reaction_zone = settings["reaction_zone"]

        # Applies volume
        self.sound_manager.set_volume(self.settings.volume)

        # Apply target score
        self.WINNING_SCORE = self.settings.target_score
        
        # Apply background speed
        self.bg_change_rate = self.settings.bg_speed_values[self.settings.bg_speed]


    def _generate_bg_colors(self):
        # List of color presets
        palette = [
            (255, 0, 0),      # Red
            (255, 128, 0),    # Orange
            (204, 0, 204),    # Magenta
            (128, 255, 0),    # Lime
            (0, 204, 0),      # Green
            (0, 204, 204),    # Cyan
            (0, 128, 255),    # Light blue
            (0, 0, 255),      # Blue
            (127, 0, 255),    # Purple
            (255, 0, 255),    # Pink
        ]
        
        # Generate random stripes
        # Also avoid generating the same color twice in a row
        num_stripes = 6 # How many stripes we want
        self.bg_colors = [] # just stores the chosen colors
        prev = None # Remembers the previous color so we dont repeat

        # Loop that repeats 6 times. Depends on num_stripes
        for _ in range(num_stripes):
            # Picks a random color
            color = random.choice(palette)
            # If the color is the same as the previous one it picks another
            # Keeps looping if we land on it again
            while color == prev:
                color = random.choice(palette)
            # Adds the color to the list
            self.bg_colors.append(color)
            # Updates the prev variable
            prev = color

        

    def handle_menu_events(self):
        # Handle input in main menu
        self.input_handler.poll()
        
        if self.input_handler.should_quit():
            self.is_running = False
            return
        
        # Moves up in the menu if up the up arrow is pressed
        if self.input_handler.is_just_pressed(InputHandler.ACTION_UP):
            self.menu.navigate(-1)
            self.sound_manager.play_menu_move()
        
        # Moves down in the menu if the down arrow is pressed
        if self.input_handler.is_just_pressed(InputHandler.ACTION_DOWN):
            self.menu.navigate(1)
            self.sound_manager.play_menu_move()
        
        # Selects the option if enter/return is pressed
        if self.input_handler.is_just_pressed(InputHandler.ACTION_CONFIRM):
            choice = self.menu.select()
            self.sound_manager.play_menu_select()
            
            # If "Start Game" is pressed the game loop starts
            if choice == "START GAME":
                self.reset_game()
                self.state = self.STATE_PLAYING
            # If "Settings" is pressed, go to settings
            elif choice == "SETTINGS":
                self.state = self.STATE_SETTINGS
            # If "Quit" is pressed then the game stops 
            elif choice == "QUIT":
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
            self.sound_manager.play_menu_move()
        
        # Move down
        if self.input_handler.is_just_pressed(InputHandler.ACTION_DOWN):
            self.settings.navigate(1)
            self.sound_manager.play_menu_move()

        # Adjusts the settings value
        # Decrease the setting value
        if self.input_handler.is_just_pressed(InputHandler.ACTION_LEFT):
            self.settings.adjust(-1) # Decreases it
            self.sound_manager.play_menu_move() # Sounds
            self.apply_settings() # Updates the game with the new settings
        
        # Increase the setting value
        if self.input_handler.is_just_pressed(InputHandler.ACTION_RIGHT):
            self.settings.adjust(1) # Increases it
            self.sound_manager.play_menu_move() # Sounds
            self.apply_settings() # Updates the game with the new settings
        
        # Confirms the selection
        if self.input_handler.is_just_pressed(InputHandler.ACTION_CONFIRM):
            choice = self.settings.select() # Gets the currently selected option
            if choice == "BACK": # if back is selected
                self.sound_manager.play_menu_select()
                self.state = self.STATE_MENU # Returns to the main menu
        
        # If back/escape is used
        if self.input_handler.is_just_pressed(InputHandler.ACTION_BACK):
            self.state = self.STATE_MENU # Back to main menu
            self.sound_manager.play_menu_select()

    def handle_game_events(self):
        # Handles the input during gameplay

        # Update the input handler for this frame (poll keyboard, etc.)
        self.input_handler.poll()

        # Quits if requested        
        if self.input_handler.should_quit():
            self.is_running = False
            return
        
        # Press space to start
        # Only does the countdown on the first round
        if self.input_handler.is_just_pressed(InputHandler.ACTION_START) or self.input_handler.is_just_pressed(InputHandler.ACTION_CONFIRM):
            if not self.ball.moving and not self.countdown_active:
                if self.first_round:
                    self.sound_manager.stop_music()
                    self.start_countdown()  
                    self.sound_manager.play_countdown()
                else:
                    self.ball.start()
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

        if self.win_music_timer > 0:
                self.win_music_timer -= 1
                if self.win_music_timer <= 0:
                    self.sound_manager.play_music()  
        
        if self.lose_music_timer > 0:
            self.lose_music_timer -= 1
            if self.lose_music_timer <= 0:
                self.sound_manager.play_music()  

        # Quits if requested
        if self.input_handler.should_quit():
            self.is_running = False
            return
        
        # Navigation

        # Move up
        if self.input_handler.is_just_pressed(InputHandler.ACTION_UP):
            self.sound_manager.play_menu_move()  
            self.end_screen.navigate(-1) # Move highlight up
        
        # Move down
        if self.input_handler.is_just_pressed(InputHandler.ACTION_DOWN):
            self.sound_manager.play_menu_move()  
            self.end_screen.navigate(1) # Move highlight down
        
        # Confirms selection
        if self.input_handler.is_just_pressed(InputHandler.ACTION_CONFIRM):
            #Gets the selected menu option
            choice = self.end_screen.select()
            self.sound_manager.play_menu_select()  
            
            # Performs a action depending on the choice
            if choice == "PLAY AGAIN":
                self.reset_game() # Resets the game state
                self.state = self.STATE_PLAYING # Back to the game
            elif choice == "MAIN MENU":
                self.reset_game() # Resets the game state
                self.state = self.STATE_MENU # Back to main menu
            elif choice == "QUIT":
                self.is_running = False # Quits game 


    def update(self):

        if self.countdown_active:
            self.countdown -= 1
            if self.countdown <= -30: # This lets the "GO!" actually appear for a bit
                self.countdown_active = False
                self.ball.start()
                self.first_round = False
                self.sound_manager.play_music()
            return  # Don't update game while counting down

        self.ball.update()
        self.ai.update()
        
        # Ball collision with top/bottom walls
        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = self.ball.radius
            self.ball.bounce_y()
            self.sound_manager.play_wall_hit()
        elif self.ball.y + self.ball.radius >= self.screen_height:
            self.ball.y = self.screen_height - self.ball.radius
            self.ball.bounce_y()
            self.sound_manager.play_wall_hit()
        
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
            self.sound_manager.play_paddle_hit()
        
        # AI paddle collision
        if ball_rect.colliderect(self.paddle2.get_bounds()) and self.ball.x_velocity > 0:
            self.ball.x = self.paddle2.x - self.ball.radius
            self.ball.bounce_x()
            self.sound_manager.play_paddle_hit()
        
        # Ball out of bounds (score)
        # Updates the scoreboard too
        
        # If the ball goes off the LEFT side of the screen
        if self.ball.x <= 0:
            # Right player scores
            self.scoreboard.score_right()
            # Win sound
            self.sound_manager.play_score()
            # Checks for win
            self.check_win_condition()
            # Only reset if game not over
            if self.state == self.STATE_PLAYING:  
                self.ball.reset(self.screen_width//2, self.screen_height//2)


        # If the ball goes off the RIGHT side of the screen
        if self.ball.x >= self.screen_width:
            # Left player scores
            self.scoreboard.score_left()
            # Checks for win
            self.check_win_condition()
            # Reset ball to the center
            if self.state == self.STATE_PLAYING:
                self.ball.reset(self.screen_width//2, self.screen_height//2)   

    def check_win_condition(self):
        # Checks if someone has won

        # Checks if player one has won
        if self.scoreboard.p1_score >= self.WINNING_SCORE:
            # Updates the end screen with the proper info 
            self.end_screen.set_winner("PLAYER 1", 
                                       self.scoreboard.p1_score, 
                                       self.scoreboard.p2_score)
            # Switches game state to end scren
            self.state = self.STATE_END
            # Music stuff
            self.sound_manager.stop_music()
            self.sound_manager.play_win()
            self.win_music_timer = 200 #  for the winner music (60FPS)

        # Checks if player two (AI) has won
        elif self.scoreboard.p2_score >= self.WINNING_SCORE:
            # Updates the end screen with the proper info 
            self.end_screen.set_winner("AI", 
                                       self.scoreboard.p1_score, 
                                       self.scoreboard.p2_score)
            # Switches gamet to end screen
            self.state = self.STATE_END
            self.sound_manager.stop_music()
            self.sound_manager.play_lose()
            self.lose_music_timer = 200 # for the loser music
    
    def render_background(self):
         # The animated background

        # Counts frames
        self.bg_timer += 1.5

        # Triggers the change once it hits the limit 
        if self.bg_timer >= self.bg_change_rate:
            self.bg_timer = 0   # Timer reset
            self._generate_bg_colors()  # New set of colors
        
        # Draw stripes
        stripe_height = self.screen_height // len(self.bg_colors)
        for i, color in enumerate(self.bg_colors):
            # Dim the colors so we don't go blind
            dimmed = (color[0] // 1.5, color[1] // 1.5, color[2] // 1.5)
            pygame.draw.rect(self.screen, dimmed, 
                            (0, i * stripe_height, self.screen_width, stripe_height))

    def render(self):
        # Draws the center dashed lines (upon gameplay)
        for y in range(0, self.screen_height, 20):
            pygame.draw.rect(self.screen, (50, 50, 50), 
                        (self.screen_width // 2 - 2, y, 4, 10))

        # Draws the scoreboard onto the screen
        self.scoreboard.render(self.screen, self.screen_width, self.WINNING_SCORE)
        
        #Draws the paddles and ball
        self.ball.render(self.screen)
        self.paddle1.render(self.screen)
        self.paddle2.render(self.screen)

       # Countdown display
        if self.countdown_active:
            # If the countdown has finished
            if self.countdown <= 0:
                text = "GO!"                 # Display "GO!" when countdown reaches 0
                color = (0, 255, 0)          # Green color for "GO!"
            else:
                # Calculates the current second to display (3, 2, or 1)
                # countdown is in frames 
                # So dividing by 60 gives approximate seconds
                seconds = (self.countdown - 1) // 60 + 1
                text = str(seconds)          # Convert the number to a string for rendering
                color = (0, 0, 0)            # Black color for countdown numbers
            
            # Render the countdown text using the countdown_font
            countdown_surf = self.countdown_font.render(text, True, color)
            # Center the text on the screen
            countdown_rect = countdown_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            # Draws the countdown text onto the screen
            self.screen.blit(countdown_surf, countdown_rect)

        # "Press SPACE to start" hint (only when the ball is stationary and the countdown isnt active)
        elif not self.ball.moving:
            font = pygame.font.Font("fonts/aa.TTF", 30)

            # Render the hint text in gray
            text = font.render("PRESS SPACE TO START", True, (100, 100, 100))
            # Position the hint at the bottom center of the screen
            rect = text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            # Draw the hint text onto the screen
            self.screen.blit(text, rect)

        #New frame, updates display
        pygame.display.flip()
    
    def reset_game(self):
        #Reset the game state for a new game

        # Reset timer
        self.win_music_timer = 0 
        self.lose_music_timer = 0

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

        # Resets so the countdown runs again
        self.first_round = True

    def run(self):
        # The main game loop
        try:
            # Keeps looping while the game is running
            while self.is_running:
                # Renders the background
                self.render_background()

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