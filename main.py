import pygame
from constants import SCREEN_HEIGHT
from constants import SCREEN_WIDTH
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from particle import Particle
from floatingtext import FloatingText
import random
import sys


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver} ")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    game_over = False
    score = 0
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, drawable, updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
    PowerUp.containers = (powerups, updatable, drawable)
    Particle.containers = (updatable, drawable)
    FloatingText.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()



    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_over and event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.lives = 3
                    score = 0
                    game_over = False
                    player.invulnerable_timer = 3.0
                    for a in asteroids:
                        a.kill()
                    for s in shots:
                        s.kill()
                    for p in powerups:
                        p.kill()



        screen.fill("black")
        if not game_over:
            updatable.update(dt)
            for a in asteroids:
                if player.invulnerable_timer <= 0 and a.collides_with(player):
                    log_event("player_hit")
                    player.lives -= 1
                    FloatingText(player.position.x, player.position.y, "-1 life", font)
                    if player.lives <= 0:
                        game_over = True


                    else:
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.invulnerable_timer = 3.0



            for powerup in powerups:
                if powerup.collides_with(player):
                    if powerup.kind == "shotgun":
                        player.shotgun_timer = 10.0  # 10 seconds of shotgun power!
                    powerup.kill()  # remove it from the screen

            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        score += 100
                        FloatingText(asteroid.position.x, asteroid.position.y, "+100", font)
                        for _ in range(15):
                            Particle(asteroid.position.x, asteroid.position.y)

                        if random.random() < 0.02:
                            PowerUp(asteroid.position.x, asteroid.position.y, "shotgun")

                        asteroid.split()
                        shot.kill()
                        break


            for d in drawable:
                d.draw(screen)
                lives_text = font.render(f"Lives: {player.lives}", True, "white")
                score_text = font.render(f"SCORE: {score}", True, "white")
                score_x = SCREEN_WIDTH - score_text.get_width()
                score_y = 10
                screen.blit(score_text, (score_x, score_y))
                screen.blit(lives_text, (10, 10))
        else:
            game_over_text = font.render("GAME OVER - Press R to Restart", True, "red")
            x = (SCREEN_WIDTH - game_over_text.get_width()) / 2
            y = (SCREEN_HEIGHT - game_over_text.get_width()) / 2
            screen.blit(game_over_text, (x, y))

        pygame.display.flip()
        dt = clock.tick(60) / 1000




if __name__ == "__main__":
    main()
