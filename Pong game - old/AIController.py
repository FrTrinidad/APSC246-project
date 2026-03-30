class AIController:
    def __init__(self, ball, paddle, screen_width):
        self.ball = ball
        self.paddle = paddle
        self.speed = 3.5 # This is the AI's movement speed (determined by difficulty)
        
        self.screen_width = screen_width
        self.reaction_zone = 0.5

    def update(self):
        # Only move if ball is coming toward AI paddle
        # Also only moves past a certain point (the reaction zone)
        if self.ball.x_velocity > 0:
            reaction_x = self.screen_width * self.reaction_zone
            if self.ball.x > reaction_x:
                self.move_decider()
    
    def move_decider(self):
        paddle_center = self.paddle.y + self.paddle.height / 2
        tolerance = 10
        
        if self.ball.y > paddle_center + tolerance:
            self.paddle.move_down()
        elif self.ball.y < paddle_center - tolerance:
            self.paddle.move_up()