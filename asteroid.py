from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
import pygame
import random
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20,50)
            new_asteroid1 = Asteroid(self.position[0], self.position[1], self.radius - ASTEROID_MIN_RADIUS)
            new_asteroid2 = Asteroid(self.position[-0], self.position[-1], self.radius - ASTEROID_MIN_RADIUS)
            new_asteroid1.velocity = pygame.math.Vector2.rotate(self.velocity, random_angle) * 2.0
            new_asteroid2 .velocity = pygame.math.Vector2.rotate(self.velocity, -random_angle) * 2.0
