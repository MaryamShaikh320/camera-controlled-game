import pygame  # noqa: I001
from player import Player
from road import Road

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GROUND_Y = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("2D Platformer")

clock = pygame.time.Clock()

player = Player()
road = Road()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
    keys = pygame.key.get_pressed()
    player.jump(keys)
    player.update(GROUND_Y)
    road.update()

    screen.fill((40, 44, 52))

    road.draw_road(screen)
    road.draw_left_divider(screen)
    road.draw_right_divider(screen)
    pygame.draw.rect(screen, (55, 204, 187), player.rect)
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()