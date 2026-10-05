from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SHOOT_SPEED
from constants import LINE_WIDTH
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED
from shot import Shot
import pygame



class Player(CircleShape):
    def __init__(self, x, y):
        self.lives = 3
        self.invulnerable_timer = 0
        self.shotgun_timer = 0
        super().__init__(x, y, PLAYER_RADIUS)
    rotation = 0
    shot_timer = 0



    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]


    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt



    def update(self, dt: float) -> None:
        self.shot_timer -= dt
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
        if self.shotgun_timer > 0:
            self.shotgun_timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_SPACE]:
            self.shoot()


    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector


    def shoot(self):
            if self.shot_timer > 0:
                return
            else:
             self.shot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS



            if self.shotgun_timer > 0:
                angles = [-15, 0, 15]
            else:
                angles = [0]

            for angle_offset in angles:
                shot = Shot(self.position.x, self.position.y)
                unit_vector = pygame.Vector2(0, 1)
                rotated_vector = unit_vector.rotate(self.rotation + angle_offset)
                shot.velocity = rotated_vector * PLAYER_SHOOT_SPEED
