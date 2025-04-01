import pygame
import random

class EnemyFish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/fish.png")
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect(center=(random.randint(0, 800), random.randint(50, 150)))
        self.speed = random.choice([2, -2])
        self.dive_speed = 1
        self.diving = False

    def update(self):
        if not self.diving:
            self.rect.x += self.speed
            if self.rect.left <= 0 or self.rect.right >= 800:
                self.speed *= -1
            if random.random() < 0.01:
                self.diving = True
        else:
            self.rect.y += self.dive_speed
            if self.rect.top >= 600:
                self.kill()
