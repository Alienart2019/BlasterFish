import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800

# Constants
PLAYER_SPEED = 7
BUBBLE_SPEED = -8
ENEMY_SPEED_BASE = 2
FPS = 60

# Damage Constants
JELLYFISH_DAMAGE = 1
CRAB_DAMAGE = 2
MYTHICAL_DAMAGE = 3
EEL_DAMAGE = 2
BOSS_DAMAGE = 4

# Load images
player_img = pygame.image.load("Playersprite.png")
bubble_img = pygame.image.load("BubbleSprites.png")
jellyfish_img = pygame.image.load("JellyFishSprite.png")
crab_img = pygame.image.load("CrabSprite.png")
mythical_img = pygame.image.load("SharkSprite.png")
eel_img = pygame.image.load("EelSprite.webp")
boss_img = pygame.image.load("BossSprite.png")
powerup_imgs = {
    "speed": pygame.image.load("SpeedBoost.png"),
    "spread": pygame.image.load("SpreadShot.png"),
    "health": pygame.image.load("HealthPack.png")
}

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blaster Fish")
clock = pygame.time.Clock()

# Colors
OCEAN_BLUE = (0, 50, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Power-Up Types
POWER_UP_TYPES = ["speed", "spread", "health"]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (100, 100))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.speed = PLAYER_SPEED
        self.health = 5
        self.spread_shot = False
        self.speed_boost_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
        else:
            self.speed = PLAYER_SPEED

    def take_damage(self, damage):
        self.health -= damage

# Bubble class
class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bubble_img, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += BUBBLE_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Enemy base class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, health, damage):
        super().__init__()
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = health
        self.damage = damage

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Enemy Types
class Jellyfish(Enemy):
    def __init__(self):
        super().__init__(jellyfish_img, random.randint(50, WIDTH - 50), 50, ENEMY_SPEED_BASE, 1, JELLYFISH_DAMAGE)
        self.direction = 1

    def update(self):
        self.rect.y += self.speed * self.direction
        if random.random() < 0.02:
            self.direction *= -1

class Crab(Enemy):
    def __init__(self):
        super().__init__(crab_img, random.randint(50, WIDTH - 50), 50, ENEMY_SPEED_BASE, 2, CRAB_DAMAGE)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1

class Mythical(Enemy):
    def __init__(self):
        super().__init__(mythical_img, random.randint(50, WIDTH - 50), 50, ENEMY_SPEED_BASE + 1, 3, MYTHICAL_DAMAGE)

class ElectricEel(Enemy):
    def __init__(self):
        super().__init__(eel_img, random.randint(50, WIDTH - 50), 50, ENEMY_SPEED_BASE + 1, 2, EEL_DAMAGE)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

# Boss
class Boss(Enemy):
    def __init__(self):
        super().__init__(boss_img, WIDTH // 2, 100, 1, 50, BOSS_DAMAGE)

    def update(self):
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed *= -1

# Power-Up
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(POWER_UP_TYPES)
        self.image = pygame.transform.scale(powerup_imgs[self.type], (50, 50))
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))

    def update(self):
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()

# Levels
LEVELS = [
    {"spawn_rate": 0.02, "enemy_types": [lambda: Jellyfish()]},
    {"spawn_rate": 0.04, "enemy_types": [lambda: Jellyfish(), lambda: Crab()]},
    {"spawn_rate": 0.06, "enemy_types": [lambda: Jellyfish(), lambda: Crab(), lambda: Mythical()]},
    {"spawn_rate": 0.07, "enemy_types": [lambda: Crab(), lambda: Mythical(), lambda: ElectricEel()]},
    {"spawn_rate": 0, "boss": True}
]

# Radar
def draw_radar(enemies, powerups):
    pygame.draw.rect(screen, (30, 30, 30), (WIDTH - 210, 10, 200, 150))
    for e in enemies:
        x = int((e.rect.centerx / WIDTH) * 200)
        y = int((e.rect.centery / HEIGHT) * 150)
        pygame.draw.circle(screen, RED, (WIDTH - 210 + x, 10 + y), 3)
    for p in powerups:
        x = int((p.rect.centerx / WIDTH) * 200)
        y = int((p.rect.centery / HEIGHT) * 150)
        pygame.draw.circle(screen, GREEN, (WIDTH - 210 + x, 10 + y), 3)

# Main game function
def main_game():
    player = Player()
    player_group = pygame.sprite.Group(player)
    bubble_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()
    boss = None

    score = 0
    level = 0
    last_shot = 0
    shoot_delay = 250
    powerup_timer = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(OCEAN_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        # Shooting
        if keys[pygame.K_SPACE] and now - last_shot > shoot_delay:
            last_shot = now
            if player.spread_shot:
                bubble_group.add(Bubble(player.rect.centerx - 20, player.rect.top))
                bubble_group.add(Bubble(player.rect.centerx, player.rect.top))
                bubble_group.add(Bubble(player.rect.centerx + 20, player.rect.top))
            else:
                bubble_group.add(Bubble(player.rect.centerx, player.rect.top))

        # Level progression
        if score >= 500 and level < 1:
            level = 1
        elif score >= 1500 and level < 2:
            level = 2
        elif score >= 2500 and level < 3:
            level = 3
        elif score >= 4000 and level < 4:
            level = 4

        if level < 4 and random.random() < LEVELS[level]["spawn_rate"]:
            enemy_group.add(random.choice(LEVELS[level]["enemy_types"])())

        # Boss battle
        if level == 4 and not boss:
            boss = Boss()
            enemy_group.add(boss)

        # Power-Up spawn
        if random.random() < 0.005:
            powerup_group.add(PowerUp())

        player_group.update()
        bubble_group.update()
        enemy_group.update()
        powerup_group.update()

        # Bubble collisions
        for bubble in bubble_group:
            hits = pygame.sprite.spritecollide(bubble, enemy_group, False)
            for enemy in hits:
                enemy.health -= 1
                if enemy.health <= 0:
                    score += 100
                    enemy.kill()
                bubble.kill()

        # Enemy collision
        hits = pygame.sprite.spritecollide(player, enemy_group, True)
        for enemy in hits:
            player.take_damage(enemy.damage)

        # Power-Up collision
        hits = pygame.sprite.spritecollide(player, powerup_group, True)
        for p in hits:
            if p.type == "health":
                player.health = min(player.health + 1, 5)
            elif p.type == "speed":
                player.speed = PLAYER_SPEED + 3
                player.speed_boost_timer = 300
            elif p.type == "spread":
                player.spread_shot = True
                pygame.time.set_timer(pygame.USEREVENT, 5000)

        # Turn off spread shot
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                player.spread_shot = False

        # Draw
        player_group.draw(screen)
        bubble_group.draw(screen)
        enemy_group.draw(screen)
        powerup_group.draw(screen)
        draw_radar(enemy_group, powerup_group)

        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Health: {player.health}", True, WHITE), (10, 50))

        if player.health <= 0:
            running = False

        pygame.display.flip()

# Run game
if __name__ == "__main__":
    main_game()
    pygame.quit()