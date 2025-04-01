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
WHITE = (255, 255, 255)

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
        self.speed = PLAYER_SPEED
        self.health = 3  # Player starts with 3 health

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def take_damage(self):
        self.health -= 1


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


# Main menu function
def main_menu():
    font = pygame.font.Font(None, 74)
    title_text = font.render("Underwater Galaga", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)

    while True:
        screen.fill(OCEAN_BLUE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start game on SPACE press
                    return
                elif event.key == pygame.K_q:  # Quit game on Q press
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(FPS)


# Game over function
def game_over(score):
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)

    while True:
        screen.fill(OCEAN_BLUE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game on R press
                    return

        pygame.display.flip()
        clock.tick(FPS)


# Main game loop function
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

        # Check for collisions between enemies and the player
        if pygame.sprite.spritecollide(player, enemy_group, True):  # Remove enemy on collision with player
            player.take_damage()
            if player.health <= 0:  # End game when health reaches zero
                game_over(score)
                return

        # Draw everything on the screen
        screen.fill(OCEAN_BLUE)  # Background color
        player_group.draw(screen)
        bubble_group.draw(screen)
        enemy_group.draw(screen)

        # Display score and health
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        health_text = font.render(f"Health: {player.health}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))

        # Refresh display and maintain framerate
        pygame.display.flip()
        clock.tick(FPS)


# Run the game!
if __name__ == "__main__":
    while True:
        main_menu()  # Show main menu first
        main_game()  # Start the main game loop after menu selection
