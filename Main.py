# Features: Player movement with touch, shoot bubble by tapping

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty

# Set default window size for PC testing
Window.size = (400, 700)

# Constants
PLAYER_SPEED = 10    # how fast player moves
BUBBLE_SPEED = 8     # how fast bubble moves up

# Class for the Bubble (your projectile)
class Bubble(Image):
    velocity = NumericProperty(0)

    def move(self):
        self.y += self.velocity  # move upward

# Class for the Player (your fish)
class Player(Image):
    def move(self, touch_x):
        self.center_x = touch_x  # move player to finger x

# Main Game class
class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load your player sprite from PC version
        self.player = Player(source="PlayerSprite2.png", size_hint=(None, None), size=(80, 80))
        self.player.center_x = self.center_x
        self.player.y = 20  # place near bottom
        self.add_widget(self.player)

        # Create a list to track bubbles
        self.bubbles = []

        # Schedule update method to run at 60 FPS
        Clock.schedule_interval(self.update, 1/60)

    def on_touch_move(self, touch):
        # When dragging finger, move player
        self.player.move(touch.x)

    def on_touch_down(self, touch):
        # When tapping screen, shoot bubble
        self.shoot_bubble()

    def shoot_bubble(self):
        # Create a bubble from your PC sprite
        bubble = Bubble(source="BubbleSprites.png", size_hint=(None, None), size=(30, 30))
        bubble.center_x = self.player.center_x
        bubble.y = self.player.top
        bubble.velocity = BUBBLE_SPEED

        # Add the bubble to screen and list
        self.bubbles.append(bubble)
        self.add_widget(bubble)

    def update(self, dt):
        # Move all bubbles
        for bubble in self.bubbles[:]:  # copy list so we can safely remove
            bubble.move()

            # Remove if bubble goes off top of screen
            if bubble.top > self.height:
                self.bubbles.remove(bubble)
                self.remove_widget(bubble)

# The App class (needed for Kivy to run)
class BlasterFishApp(App):
    def build(self):
        return Game()

# Run the App
if __name__ == "__main__":
    BlasterFishApp().run()
