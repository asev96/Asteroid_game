import pygame
from constants import SCREEN_HEIGHT
from constants import SCREEN_WIDTH
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver} ")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    game_over = False
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, drawable, updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
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
                    game_over = False
                    player.invulnerable_timer = 3.0
                    for a in asteroids:
                        a.kill()
                    for s in shots:
                        s.kill()



        screen.fill("black")
        if not game_over:
            updatable.update(dt)
            for a in asteroids:
                if player.invulnerable_timer <= 0 and a.collides_with(player):
                    log_event("player_hit")
                    player.lives -= 1
                    if player.lives <= 0:
                        game_over = True


                    else:
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.invulnerable_timer = 3.0



            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()


            for d in drawable:
                d.draw(screen)
                lives_text = font.render(f"Lives: {player.lives}", True, "white")
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
