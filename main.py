import pygame  # noqa: I001
from player import Player
from road import Road
from obstacle import Obstacle
from coin import Coin
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GROUND_Y = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Psedo 3D Game")

clock = pygame.time.Clock()

player = Player()
road = Road()

obstacles = []
OBSTACLE_SPAWN_INTERVAL = 1000
obstacle_last_spawn_time = 0

coins = []
coin_count = 0
COIN_SPAWN_INTERVAL = 500
coin_last_spawn_time = 0

game_over = False


def reset_game():
    global player, road, obstacles, coins, coin_count, game_over
    global obstacle_last_spawn_time, coin_last_spawn_time
    
    player = Player()
    road = Road()
    obstacles = []
    coins = []
    coin_count = 0
    game_over = False
    obstacle_last_spawn_time = pygame.time.get_ticks()
    coin_last_spawn_time = pygame.time.get_ticks()


def spawn_obstacles():
    num_obstacles = random.randint(1, 2)

    for lane in random.sample([0, 1, 2], num_obstacles):
        obstacles.append(Obstacle(lane, road))

def spawn_coins():
    lane = random.randint(0, 2)
    coins.append(Coin(lane, road))


font = pygame.font.Font(None, 36)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()
            else:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

    if not game_over:
        current_time = pygame.time.get_ticks()
        if (current_time - obstacle_last_spawn_time) >= OBSTACLE_SPAWN_INTERVAL:
            spawn_obstacles()
            obstacle_last_spawn_time = current_time
        if (current_time - coin_last_spawn_time) >= COIN_SPAWN_INTERVAL:
            spawn_coins()
            coin_last_spawn_time = current_time

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
                    game_over = True

        for coin in coins[:]:
            coin.update()

            if coin.progress >= 1:
                coins.remove(coin)
                continue

            if coin.is_at_player(GROUND_Y) and coin.lane == player.current_lane and player.jump_height < 40:
                    coin_count += 1
                    coins.remove(coin)

    screen.fill((40, 44, 52))

    road.draw_road(screen)
    road.draw_left_divider(screen)
    road.draw_right_divider(screen)

    for obstacle in obstacles:
        obstacle.draw(screen)

    for coin in coins:
        coin.draw(screen)

    player.draw(screen)

    coin_text = font.render(f"Score: {coin_count}", True, (255, 190, 40))
    screen.blit(coin_text, (20, 30))

    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        game_over_text = font.render("GAME OVER", True, (255, 80, 80))
        restart_text = font.render("Press Space to Restart", True, (255, 255, 255))
        final_score_text = font.render(
            f"Coins Collected: {coin_count}",
            True,
            (255, 190, 40)
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        )
        screen.blit(
            restart_text,
            restart_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        )
        screen.blit(
            final_score_text,
            final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
