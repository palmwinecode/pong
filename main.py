from kivy.app import App # type: ignore
from kivy.uix.widget import Widget # type: ignore
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty # type: ignore
from kivy.vector import Vector # type: ignore
from kivy.clock import Clock # type: ignore

class PongPaddle(Widget):
    # Create a score numberic property
    score = NumericProperty(0)

    # Function to bounce ball
    def bounce_ball(self, ball):
        # Did ball hot paddle?
        if self.collide_widget(ball):
            # Bounce algorithm(can be better?)
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball on step. This
    # will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos 

class PongGame(Widget):

    # Create object properties
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    # Function to serve ball
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    # Function to update state of the game
    def update(self, dt):
        self.ball.move()

        # Bounce off the paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # Went off to the side to score a point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))

        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    # Function to handle drag event
    def on_touch_move(self, touch):
        # Check for postion of touch
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
        
# Base class
class PongApp(App):

    def build(self):
        # Create an object of the game
        game = PongGame()

        # Call serve_ball method of the game object
        game.serve_ball()

        # Call the update function of the game object 60 times a second
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
        
# Run Base class
if __name__ == "__main__":
    PongApp().run()