import pygame
from constants import *
from shot import Shot

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (255, 255, 255), [(20, 0), (0, 40), (40, 40)], 2)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Rotate left
            self.rotation += PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d]:  # Rotate right
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_w]:  # Move forward
            acceleration = pygame.Vector2(0, -PLAYER_SPEED).rotate(-self.rotation)
            self.velocity += acceleration * dt

        self.velocity *= 0.98  # Add some drag

        self.position += self.velocity * dt
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)

    def shoot(self):
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        shot_pos = self.position + forward * 20
        shot_velocity = forward * PLAYER_SHOOT_SPEED + self.velocity
        return Shot(shot_pos.x, shot_pos.y, shot_velocity)

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)
    
    def reset(self):
        self.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.rect.center = self.position