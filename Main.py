# Full Blaster Fish Mobile Game
# Features: player, bubbles, enemies, collision, score, health, level system, boss

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty
import random

# Set window size for PC testing
Window.size = (400, 700)

# Constants
PLAYER_SPEED = 10
BUBBLE_SPEED = 8
BASE_ENEMY_SPEED = 3
SPAWN_INTERVAL = 1.5  # base spawn rate

# Class for Bubble (bullet)
class Bubble(Image):
    velocity = NumericProperty(0)

    def move(self):
        self.y += self.velocity

# Class for Player (fish)
class Player(Image):
    def move(self, touch_x):
        self.center_x = touch_x

# Class for Enemy (any enemy type)
class Enemy(Image):
    velocity = NumericProperty(0)
    enemy_type = ""  # jellyfish, crab, shark, eel, boss

    def move(self):
        self.y -= self.velocity

# Main Game
class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add background
        self.background = Image(source="Background.png",
                                 allow_stretch=True, keep_ratio=False,
                                 size_hint=(None, None),
                                 size=Window.size,
                                 pos=(0, 0))
        self.add_widget(self.background)

        # Add player
        self.player = Player(source="PlayerSprite2.png", size_hint=(None, None), size=(80, 80))
        self.player.center_x = self.center_x
        self.player.y = 20
        self.add_widget(self.player)

        # Initialize lists
        self.bubbles = []
        self.enemies = []

        # Initialize score, health, level
        self.score = 0
        self.health = 5
        self.level = 1
        self.enemy_speed = BASE_ENEMY_SPEED
        self.spawn_interval = SPAWN_INTERVAL

        # Score and health display
        self.score_label = Label(text=f"Score: {self.score}", pos=(10, 660), size_hint=(None, None), font_size=24, color=(1,1,1,1))
        self.health_label = Label(text=f"Health: {self.health}", pos=(10, 630), size_hint=(None, None), font_size=24, color=(1,1,1,1))
        self.level_label = Label(text=f"Level: {self.level}", pos=(300, 660), size_hint=(None, None), font_size=24, color=(1,1,1,1))
        self.add_widget(self.score_label)
        self.add_widget(self.health_label)
        self.add_widget(self.level_label)

        # Schedule updates
        Clock.schedule_interval(self.update, 1/60)  # 60 FPS
        Clock.schedule_interval(self.spawn_enemy, self.spawn_interval)  # spawn enemies

    def on_touch_move(self, touch):
        self.player.move(touch.x)

    def on_touch_down(self, touch):
        self.shoot_bubble()

    def shoot_bubble(self):
        bubble = Bubble(source="BubbleSprites.png", size_hint=(None, None), size=(30, 30))
        bubble.center_x = self.player.center_x
        bubble.y = self.player.top
        bubble.velocity = BUBBLE_SPEED
        self.bubbles.append(bubble)
        self.add_widget(bubble)

    def spawn_enemy(self, dt):
        # Choose enemy based on level
        if self.level < 5:
            enemy_choice = random.choice(["jellyfish", "crab", "mythical", "eel"])
        else:
            enemy_choice = "boss"  # level 5 = boss

        # Assign properties based on enemy
        if enemy_choice == "jellyfish":
            image_source = "JellyFishSprite.png"
            size = (70, 70)
            speed = self.enemy_speed
        elif enemy_choice == "crab":
            image_source = "CrabSprite.png"
            size = (90, 90)
            speed = self.enemy_speed + 1
        elif enemy_choice == "mythical":
            image_source = "SharkSprite.png"
            size = (100, 100)
            speed = self.enemy_speed + 2
        elif enemy_choice == "eel":
            image_source = "EelSprite.png"
            size = (80, 80)
            speed = self.enemy_speed + 1
        elif enemy_choice == "boss":
            image_source = "BossSprite.png"
            size = (150, 150)
            speed = self.enemy_speed - 1  # boss moves slower

        # Create enemy
        enemy = Enemy(source=image_source, size_hint=(None, None), size=size)
        enemy.x = random.randint(0, self.width - enemy.width)
        enemy.top = self.height
        enemy.velocity = speed
        enemy.enemy_type = enemy_choice

        self.enemies.append(enemy)
        self.add_widget(enemy)

    def update(self, dt):
        # Move bubbles
        for bubble in self.bubbles[:]:
            bubble.move()
            if bubble.top > self.height:
                self.bubbles.remove(bubble)
                self.remove_widget(bubble)

        # Move enemies
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.y < 0:
                self.enemies.remove(enemy)
                self.remove_widget(enemy)
                self.health -= 1
                self.update_labels()

        # Check for collisions
        for enemy in self.enemies[:]:
            for bubble in self.bubbles[:]:
                if enemy.collide_widget(bubble):
                    self.handle_collision(enemy)
                    self.bubbles.remove(bubble)
                    self.remove_widget(bubble)
                    break

        # Check health
        if self.health <= 0:
            self.game_over()

    def handle_collision(self, enemy):
        # Award points based on enemy type
        if enemy.enemy_type == "jellyfish":
            self.score += 10
        elif enemy.enemy_type == "crab":
            self.score += 20
        elif enemy.enemy_type == "mythical":
            self.score += 30
        elif enemy.enemy_type == "eel":
            self.score += 15
        elif enemy.enemy_type == "boss":
            self.score += 100
            self.level_up()

        self.enemies.remove(enemy)
        self.remove_widget(enemy)
        self.update_labels()

    def update_labels(self):
        self.score_label.text = f"Score: {self.score}"
        self.health_label.text = f"Health: {self.health}"

    def level_up(self):
        self.level += 1
        self.level_label.text = f"Level: {self.level}"

        # Harder levels
        if self.spawn_interval > 0.5:
            self.spawn_interval -= 0.2
        self.enemy_speed += 1

        # Restart enemy spawning with new difficulty
        Clock.unschedule(self.spawn_enemy)
        Clock.schedule_interval(self.spawn_enemy, self.spawn_interval)

    def game_over(self):
        # Stop everything and show Game Over
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        self.clear_widgets()
        game_over_label = Label(text="GAME OVER", font_size=48, pos=(100, 350), color=(1,0,0,1))
        self.add_widget(game_over_label)

# App class
class BlasterFishApp(App):
    def build(self):
        return Game()

# Run the app
if __name__ == "__main__":
    BlasterFishApp().run()
