import pygame
import random
from circleshape import CircleShape

class Particle(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 2)  # Tiny radius (2 pixels)
        # Give it a random speed and a random angle
        speed = random.uniform(50, 200)
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(0, 1).rotate(angle) * speed
        # Lifespan in seconds
        self.lifetime = random.uniform(0.3, 0.6)

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        # Draw as an orange, yellow, or white speck
        pygame.draw.circle(screen, "orange", self.position, self.radius)
