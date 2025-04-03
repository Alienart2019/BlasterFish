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
player_img = pygame.image.load("Playersprite.png")  # Player sprite
bubble_img = pygame.image.load("BubbleSprites.png")  # Bubble projectile
jellyfish_img = pygame.image.load("JellyFishSprite.png")  # Jellyfish enemy
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

# Initialize Pygame
pygame.init()

# Screen setup using imported WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blaster Fish")
clock = pygame.time.Clock()
FPS = 60

# Colors
OCEAN_BLUE = (0, 50, 100)
WHITE = (255, 255, 255)

# Difficulty Levels
LEVELS = [
    {"spawn_rate": 0.02, "enemy_types": [Jellyfish]},
    {"spawn_rate": 0.04, "enemy_types": [Jellyfish, Crab]},
    {"spawn_rate": 0.06, "enemy_types": [Jellyfish, Crab, Mythical]},
]


def main_game():
    # Initialize sprite groups
    player_group = pygame.sprite.Group()
    bubble_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    # Create player instance
    player = Player()
    player_group.add(player)

    # Game variables
    score = 0
    level = 0  # Start at level 0
    spawn_rate = LEVELS[level]["spawn_rate"]
    enemy_types = LEVELS[level]["enemy_types"]

    last_shot_time = 0
    SHOOT_DELAY = 250  # milliseconds

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Shooting with cooldown
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > SHOOT_DELAY:
                bubble = Bubble(player.rect.centerx, player.rect.top)
                bubble_group.add(bubble)
                last_shot_time = current_time

        # Increase difficulty based on score
        if score > 500 and level == 0:
            level = 1
            spawn_rate = LEVELS[level]["spawn_rate"]
            enemy_types = LEVELS[level]["enemy_types"]
        elif score > 1500 and level == 1:
            level = 2
            spawn_rate = LEVELS[level]["spawn_rate"]
            enemy_types = LEVELS[level]["enemy_types"]

        # Spawn enemies
        if random.random() < spawn_rate:
            enemy_class = random.choice(enemy_types)
            enemy = enemy_class()
            enemy_group.add(enemy)

        # Update all sprites
        player_group.update()
        bubble_group.update()
        enemy_group.update()

        # Check collisions between bubbles and enemies
        for bubble in bubble_group:
            hits = pygame.sprite.spritecollide(bubble, enemy_group, False)
            for hit in hits:
                hit.health -= 1
                if hit.health <= 0:
                    hit.kill()
                    score += 100
                bubble.kill()

        # Check collisions between enemies and the player.
        # Sum the damage from all collided enemies.
        collided_enemies = pygame.sprite.spritecollide(player, enemy_group, True)
        if collided_enemies:
            total_damage = sum(enemy.damage for enemy in collided_enemies)
            player.take_damage(total_damage)
            if player.health <= 0:
                running = False  # End game when health is zero

        # Drawing the game elements
        screen.fill(OCEAN_BLUE)
        player_group.draw(screen)
        bubble_group.draw(screen)
        enemy_group.draw(screen)

        # Display score and health
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        health_text = font.render(f"Health: {player.health}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    while True:
        main_game()
