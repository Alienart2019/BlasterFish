import pygame
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
eel_img = pygame.image.load("EelSprite.png")
boss_img = pygame.image.load("BossSprite.png")
background_img = pygame.image.load("Background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

powerup_imgs = {
    "speed": pygame.image.load("SpeedSprite.png"),
    "spread": pygame.image.load("SpreadShotSprite.png"),
    "health": pygame.image.load("HealthSprite.png")
}

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blaster Fish")
clock = pygame.time.Clock()

# Colors
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


class Boss(Enemy):
    def __init__(self):
        super().__init__(boss_img, WIDTH // 2, 100, 1, 50, BOSS_DAMAGE)

    def update(self):
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed *= -1


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


# Levels with names and descriptions
LEVELS = [
    {"name": "Shallow Reef", "description": "Jellyfish invade!", "spawn_rate": 0.02,
     "enemy_types": [lambda: Jellyfish()]},
    {"name": "Crabby Coast", "description": "Now with crabs!", "spawn_rate": 0.04,
     "enemy_types": [lambda: Jellyfish(), lambda: Crab()]},
    {"name": "Mythic Depths", "description": "Mythical beasts approach.", "spawn_rate": 0.06,
     "enemy_types": [lambda: Jellyfish(), lambda: Crab(), lambda: Mythical()]},
    {"name": "Electric Abyss", "description": "Eels join the chaos.", "spawn_rate": 0.07,
     "enemy_types": [lambda: Crab(), lambda: Mythical(), lambda: ElectricEel()]},
    {"name": "The Deep", "description": "Face the boss!", "spawn_rate": 0, "boss": True},
    {"name": "Toxic Trench", "description": "More aggressive eels swarm in.", "spawn_rate": 0.09,
     "enemy_types": [lambda: ElectricEel(), lambda: Crab()]},
    {"name": "Shark Storm", "description": "Mythical creatures dominate.", "spawn_rate": 0.1,
     "enemy_types": [lambda: Mythical(), lambda: ElectricEel()]},
    {"name": "Crimson Cascade", "description": "Wave after wave... survive!", "spawn_rate": 0.13,
     "enemy_types": [lambda: Jellyfish(), lambda: Crab(), lambda: ElectricEel(), lambda: Mythical()]},
    {"name": "Return of the Boss", "description": "An even stronger boss returns!", "spawn_rate": 0, "boss": True},
]


def main_game(start_level=0):
    player = Player()
    player_group = pygame.sprite.Group(player)
    bubble_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()
    boss = None

    score = 0
    level = start_level
    last_shot = 0
    shoot_delay = 250

    SCORE_THRESHOLD_PER_LEVEL = 2500
    level_up_timer = 0
    level_up_display_time = 120  # ~2 seconds at 60 FPS

    bubble_particles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(30)]

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(background_img, (0, 0))

        for b in bubble_particles:
            pygame.draw.circle(screen, (173, 216, 230), (b[0], b[1]), 3)
            b[1] -= 1
            if b[1] < 0:
                b[0] = random.randint(0, WIDTH)
                b[1] = HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and now - last_shot > shoot_delay:
            last_shot = now
            if player.spread_shot:
                bubble_group.add(Bubble(player.rect.centerx - 20, player.rect.top))
                bubble_group.add(Bubble(player.rect.centerx, player.rect.top))
                bubble_group.add(Bubble(player.rect.centerx + 20, player.rect.top))
            else:
                bubble_group.add(Bubble(player.rect.centerx, player.rect.top))

        # Spawn enemies based on level
        if level < 4 and random.random() < LEVELS[level]["spawn_rate"]:
            enemy_group.add(random.choice(LEVELS[level]["enemy_types"])())

        if level == 4 and not boss:
            boss = Boss()
            enemy_group.add(boss)

        # Random power-up spawn
        if random.random() < 0.005:
            powerup_group.add(PowerUp())

        # Update all groups
        player_group.update()
        bubble_group.update()
        enemy_group.update()
        powerup_group.update()

        # Bubble hits enemy
        for bubble in bubble_group:
            hits = pygame.sprite.spritecollide(bubble, enemy_group, False)
            for enemy in hits:
                enemy.health -= 1
                if enemy.health <= 0:
                    score += 100
                    enemy.kill()
                bubble.kill()

        # Enemies hit player
        hits = pygame.sprite.spritecollide(player, enemy_group, True)
        for enemy in hits:
            player.take_damage(enemy.damage)

        # Player gets power-ups
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

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                player.spread_shot = False

        # LEVEL PROGRESSION
        if level < len(LEVELS) - 1:
            if (not LEVELS[level].get("boss") and score >= (level + 1) * SCORE_THRESHOLD_PER_LEVEL) or \
               (LEVELS[level].get("boss") and boss is None):
                level += 1
                enemy_group.empty()
                level_up_timer = level_up_display_time

        # Draw all sprites
        player_group.draw(screen)
        bubble_group.draw(screen)
        enemy_group.draw(screen)
        powerup_group.draw(screen)

        # UI: Score & Health
        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Health: {player.health}", True, WHITE), (10, 50))

        # LEVEL UP! message
        if level_up_timer > 0:
            level_up_font = pygame.font.Font(None, 64)
            level_name = LEVELS[level]["name"]
            level_text = level_up_font.render(f"Level {level + 1}: {level_name}!", True, (255, 255, 0))
            level_up_label = level_up_font.render("LEVEL UP!", True, (255, 100, 100))
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(level_up_label, (WIDTH // 2 - level_up_label.get_width() // 2, HEIGHT // 2 - 20))
            level_up_timer -= 1

        if player.health <= 0:
            running = False

        pygame.display.flip()



def launch_tkinter_menu():
    def start_game():
        selected = level_var.get()
        start_level = int(selected.split(":")[0])
        root.destroy()
        main_game(start_level=start_level)

    root = tk.Tk()
    root.title("Blaster Fish - Level Select")
    root.geometry("500x400")
    root.configure(bg="#003366")

    tk.Label(root, text="✨ Blaster Fish ✨", font=("Courier", 24, "bold"), fg="#00ffff", bg="#003366").pack(pady=10)
    tk.Label(root, text="Choose Your Starting Level", font=("Courier", 14), fg="white", bg="#003366").pack(pady=5)

    level_var = tk.StringVar()
    level_options = [
        f"{i}: {LEVELS[i]['name']} - {LEVELS[i]['description']}" for i in range(len(LEVELS))
    ]
    ttk.Combobox(root, textvariable=level_var, values=level_options, state="readonly", width=60).pack(pady=20)
    level_var.set(level_options[0])

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", foreground="#003366", background="#00ffff", font=("Courier", 12, "bold"))

    ttk.Button(root, text="🐟 Start Game 🐟", command=start_game).pack(pady=30)
    root.mainloop()


if __name__ == "__main__":
    launch_tkinter_menu()
    pygame.quit()
