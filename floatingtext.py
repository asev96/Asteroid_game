import pygame

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text="+100", font=None):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.font = font or pygame.font.Font(None, 24)
        self.image = self.font.render(text, True, "green")
        self.position = pygame.Vector2(x, y)
        self.lifetime = 0.6  # Show for 0.6 seconds
        self.speed = 40      # Float upward speed

    def update(self, dt):
        # Float upward (decreasing y)
        self.position.y -= self.speed * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))
