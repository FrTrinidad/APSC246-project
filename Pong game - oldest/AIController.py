class AIController:
    def __init__(self, ball, paddle):
        self.ball = ball
        self.paddle = paddle
    
    def update(self):
        # Only move if ball is coming toward AI paddle
        if self.ball.x_velocity > 0:
            self.move_decider()
    
    def move_decider(self):
        paddle_center = self.paddle.y + self.paddle.height / 2
        tolerance = 10
        
        if self.ball.y > paddle_center + tolerance:
            self.paddle.move_down()
        elif self.ball.y < paddle_center - tolerance:
            self.paddle.move_up()