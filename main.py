import pygame  # noqa: I001
from player import Player
from road import Road
from obstacle import Obstacle
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GROUND_Y = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("2D Platformer")

clock = pygame.time.Clock()

player = Player()
road = Road()

obstacles = []

SPAWN_INTERVAL = 1000
last_spawn_time = 0


def spawn_obstacles():
    num_obstacles = random.randint(1, 2)

    for lane in random.sample([0, 1, 2], num_obstacles):
        obstacles.append(Obstacle(lane, road))


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

    current_time = pygame.time.get_ticks()
    if (current_time - last_spawn_time) >= SPAWN_INTERVAL:
        spawn_obstacles()
        last_spawn_time = current_time

    keys = pygame.key.get_pressed()
    player.jump(keys)
    player.update(GROUND_Y)
    road.update()

    for obstacle in obstacles[:]:
        obstacle.update()

        if obstacle.progress >= 1:
            obstacles.remove(obstacle)
        elif obstacle.is_at_player(GROUND_Y) and obstacle.lane == player.current_lane:
            required_jump_height = GROUND_Y - obstacle.get_rect().top

            if player.jump_height <= required_jump_height:
                print("GAME OVER")

    screen.fill((40, 44, 52))

    road.draw_road(screen)
    road.draw_left_divider(screen)
    road.draw_right_divider(screen)

    for obstacle in obstacles:
        obstacle.draw(screen)

    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
