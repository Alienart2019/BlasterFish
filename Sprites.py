import pygame
import random

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Speed and Damage Constants
PLAYER_SPEED = 7
BUBBLE_SPEED = -8
ENEMY_SPEED_BASE = 2  # Base enemy speed
JELLYFISH_DAMAGE = 1
CRAB_DAMAGE = 2
MYTHICAL_DAMAGE = 3

# Load images
player_img = pygame.image.load("player.png")  # Player sprite
bubble_img = pygame.image.load("bubble.png")  # Bubble projectile
jellyfish_img = pygame.image.load("jellyfish.png")  # Jellyfish enemy
crab_img = pygame.image.load("crab.png")  # Crab enemy
mythical_img = pygame.image.load("mythical.png")  # Mythical creature enemy


# Player class (submarine)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 30))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = PLAYER_SPEED
        self.health = 5  # Increased health for more challenge

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def take_damage(self, damage):
        self.health -= damage


# Bubble class (projectile)
class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bubble_img, (10, 10))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += BUBBLE_SPEED
        if self.rect.bottom < 0:
            self.kill()


# Base Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, health, damage):
        super().__init__()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = health
        self.damage = damage

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Jellyfish enemy - Moves up and down
class Jellyfish(Enemy):
    def __init__(self):
        super().__init__(jellyfish_img, random.randint(50, WIDTH - 50), random.randint(50, 150),
                         ENEMY_SPEED_BASE, 1, JELLYFISH_DAMAGE)
        self.direction = 1

    def update(self):
        self.rect.y += self.speed * self.direction
        if random.random() < 0.02:  # Randomly changes direction
            self.direction *= -1


# Crab enemy - Moves side to side
class Crab(Enemy):
    def __init__(self):
        super().__init__(crab_img, random.randint(50, WIDTH - 50), random.randint(50, 150),
                         ENEMY_SPEED_BASE, 2, CRAB_DAMAGE)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1  # Bounces off walls


# Mythical creature - Moves fast and fires projectiles
class Mythical(Enemy):
    def __init__(self):
        super().__init__(mythical_img, random.randint(50, WIDTH - 50), random.randint(50, 150),
                         ENEMY_SPEED_BASE + 1, 3, MYTHICAL_DAMAGE)

    def update(self):
        self.rect.y += self.speed
        if random.random() < 0.01:  # Occasionally fires a projectile
            enemy_bubble = Bubble(self.rect.centerx, self.rect.bottom)
            return enemy_bubble
