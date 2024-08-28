import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position

    def draw(self, screen):
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius, 1)
        screen.blit(self.image, self.rect)