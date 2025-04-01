import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 7
BUBBLE_SPEED = -8
ENEMY_SPEED = 2

# Colors
OCEAN_BLUE = (0, 50, 100)
BUBBLE_COLOR = (173, 216, 230)
PLAYER_COLOR = (0, 255, 255)
ENEMY_COLOR = (255, 255, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Underwater Galaga")
clock = pygame.time.Clock()

# Player class (submarine)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

# Bubble class (projectile)
class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BUBBLE_COLOR, (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += BUBBLE_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Enemy class (fish)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(50, 150)))

    def update(self):
        self.rect.y += ENEMY_SPEED
        if self.rect.top > HEIGHT:
            self.kill()

# Initialize sprite groups
player_group = pygame.sprite.Group()
bubble_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Create player instance
player = Player()
player_group.add(player)

# Game variables
score = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Shoot bubbles when space is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bubble = Bubble(player.rect.centerx, player.rect.top)
        bubble_group.add(bubble)

    # Spawn enemies randomly
    if random.random() < 0.02:  # Adjust spawn rate as needed
        enemy = Enemy()
        enemy_group.add(enemy)

    # Update all sprites
    player_group.update()
    bubble_group.update()
    enemy_group.update()

    # Check for collisions between bubbles and enemies
    for bubble in bubble_group:
        hits = pygame.sprite.spritecollide(bubble, enemy_group, True)  # Remove enemy on collision
        if hits:
            bubble.kill()
            score += len(hits) * 100

    # Draw everything on the screen
    screen.fill(OCEAN_BLUE)  # Background color
    player_group.draw(screen)
    bubble_group.draw(screen)
    enemy_group.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Refresh display and maintain framerate
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
