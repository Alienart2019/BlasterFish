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
player_img = pygame.image.load("Playersprite2.png")
bubble_img = pygame.image.load("BubbleSprites.png")
jellyfish_img = pygame.image.load("JellyFishSprite.png")
crab_img = pygame.image.load("CrabSprite.png")
mythical_img = pygame.image.load("SharkSprite.png")
eel_img = pygame.image.load("EelSprite.png")
boss_img = pygame.image.load("BossSprite.png")

# Load different backgrounds for each level
background_imgs = [
    pygame.transform.scale(pygame.image.load("Background.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Background2.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Background3.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Background4.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Background4.png"), (WIDTH, HEIGHT))  # Placeholder reuse for boss level
]

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
DARK_BLUE = (25, 25, 112)
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
        self.image.fill(DARK_BLUE, special_flags=pygame.BLEND_RGB_MULT)
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
    {"name": "Shallow Reef", "description": "Jellyfish invade!", "spawn_rate": 0.02, "enemy_types": [lambda: Jellyfish()]},
    {"name": "Crabby Coast", "description": "Now with crabs!", "spawn_rate": 0.03, "enemy_types": [lambda: Jellyfish(), lambda: Crab()]},
    {"name": "Mythic Depths", "description": "Mythical beasts approach.", "spawn_rate": 0.04, "enemy_types": [lambda: Jellyfish(), lambda: Crab(), lambda: Mythical()]},
    {"name": "Electric Abyss", "description": "Eels join the chaos.", "spawn_rate": 0.05, "enemy_types": [lambda: Crab(), lambda: Mythical(), lambda: ElectricEel()]},
    {"name": "The Deep", "description": "Face the boss!", "spawn_rate": 0, "boss": True},
    {"name": "Twilight Trench", "description": "Enemies grow fiercer.", "spawn_rate": 0.06, "enemy_types": [lambda: Crab(), lambda: Mythical(), lambda: ElectricEel()]},
    {"name": "Abyssal Rift", "description": "Swarm attack!", "spawn_rate": 0.07, "enemy_types": [lambda: Jellyfish(), lambda: ElectricEel(), lambda: Crab()]},
    {"name": "Frozen Deep", "description": "It's getting cold...", "spawn_rate": 0.08, "enemy_types": [lambda: Mythical(), lambda: ElectricEel()]},
    {"name": "Return of the Boss", "description": "The boss returns!", "spawn_rate": 0, "boss": True}
]

def fade_transition():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300, 10):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

# Main game function

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
    bubble_particles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(30)]

    running = True
    while running:
        clock.tick(FPS)
        bg_image = background_imgs[level % len(background_imgs)]
        screen.blit(bg_image, (0, 0))

        for b in bubble_particles:
            pygame.draw.circle(screen, DARK_BLUE, (b[0], b[1]), 3)
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

        # Enemy spawning logic
        if level < 4:
            if level == 0 and random.random() < 0.02:
                enemy_group.add(Jellyfish())
            elif level > 0 and random.random() < 0.02:
                enemy_group.add(random.choice([Crab(), Mythical(), ElectricEel()]))

        # Boss level with reinforcements
        if level >= 4 and LEVELS[level % len(background_imgs)].get("boss"):
            if not boss:
                boss = Boss()
                enemy_group.add(boss)
            if random.random() < 0.03:
                enemy_group.add(random.choice([Jellyfish(), Crab(), ElectricEel(), Mythical()]))

        # Less powerups early game
        powerup_chance = 0.002 if level < 3 else 0.005
        if random.random() < powerup_chance:
            powerup_group.add(PowerUp())

        player_group.update()
        bubble_group.update()
        enemy_group.update()
        powerup_group.update()

        for bubble in bubble_group:
            hits = pygame.sprite.spritecollide(bubble, enemy_group, False)
            for enemy in hits:
                enemy.health -= 1
                if enemy.health <= 0:
                    score += 100
                    enemy.kill()
                bubble.kill()

        hits = pygame.sprite.spritecollide(player, enemy_group, True)
        for enemy in hits:
            player.take_damage(enemy.damage)

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

        player_group.draw(screen)
        bubble_group.draw(screen)
        enemy_group.draw(screen)
        powerup_group.draw(screen)


        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Health: {player.health}", True, WHITE), (10, 50))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 90))

        # Slower level progression
        if level < len(background_imgs) - 1 and score > (level + 1) * 1000:
            level += 1
            fade_transition()

        if player.health <= 0:
            running = False

        pygame.display.flip()


# Tkinter menu
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
    level_options = [f"{i}: {LEVELS[i]['name']} - {LEVELS[i]['description']}" for i in range(len(LEVELS))]
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
