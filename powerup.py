import pygame
from circleshape import CircleShape

class PowerUp(CircleShape):
    def __init__(self, x, y, kind="shotgun"):
        super().__init__(x, y, 10)  # radius of 10 pixels
        self.kind = kind

    def draw(self, screen):
        # Let's draw it as a bright yellow circle
        pygame.draw.circle(screen, "yellow", self.position, self.radius, 2)

    def update(self, dt):
        pass
