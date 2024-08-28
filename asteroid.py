import pygame
import random
from constants import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, velocity):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (radius, radius), radius, 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.radius = radius

    def update(self, dt):
        self.position += self.velocity * dt
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
        self.rect.center = self.position

    @staticmethod
    def spawn_asteroid(speed):
        side = random.choice(['left', 'top', 'right', 'bottom'])
        if side == 'left':
            x, y = 0, random.randint(0, SCREEN_HEIGHT)
            velocity = pygame.Vector2(speed, random.uniform(-speed/2, speed/2))
        elif side == 'top':
            x, y = random.randint(0, SCREEN_WIDTH), 0
            velocity = pygame.Vector2(random.uniform(-speed/2, speed/2), speed)
        elif side == 'right':
            x, y = SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
            velocity = pygame.Vector2(-speed, random.uniform(-speed/2, speed/2))
        else:  # bottom
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
            velocity = pygame.Vector2(random.uniform(-speed/2, speed/2), -speed)

        radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
        return Asteroid(x, y, radius, velocity)