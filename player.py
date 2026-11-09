
import pygame


class Player:
    def __init__(self):
        self.rect = pygame.Rect(280, 550, 50, 50)

        # Jump physics
        self.vertical_velocity = 0
        self.on_ground = True
        self.gravity = 1
        self.jump_velocity = -15
        self.jump_height = 0

        # Lane movement
        self.current_lane = 1
        self.lane_positions = [80, 280, 480]

        self.glow_surface = self.create_glow()

    def update(self, ground_y):
        self.rect.bottom = ground_y

        if not self.on_ground:
            self.vertical_velocity += self.gravity
            self.jump_height -= self.vertical_velocity

            if self.jump_height <= 0 and self.vertical_velocity > 0:
                self.jump_height = 0
                self.vertical_velocity = 0
                self.on_ground = True

    def get_hitbox(self):
        return self.rect

    def move_left(self):
        self.current_lane = max(0, self.current_lane - 1)
        self.rect.x = self.lane_positions[self.current_lane]

    def move_right(self):
        self.current_lane = min(self.current_lane + 1, 2)
        self.rect.x = self.lane_positions[self.current_lane]

    def jump(self, keys):
        if keys[pygame.K_UP] and self.on_ground:
            self.vertical_velocity = self.jump_velocity
            self.on_ground = False

    def draw(self, screen):
        visual_rect = self.rect.copy()
        visual_rect.y -= int(self.jump_height)

        glow_x = visual_rect.centerx - 50
        glow_y = visual_rect.centery - 50

        screen.blit(self.glow_surface, (glow_x, glow_y))

        pygame.draw.rect(
            screen, (41, 255, 139), visual_rect, 0, 15
        )

        pygame.draw.ellipse(
            screen,
            (160, 255, 190),
            (visual_rect.left + 3, visual_rect.top + 5, 20, 7)
        )

    def create_glow(self):
        size = 100
        center = size / 2
        radius = size / 2

        glow = pygame.Surface((size, size), pygame.SRCALPHA)

        for x in range(size):
            for y in range(size):
                distance = ((x - center) ** 2 + (y - center) ** 2) ** 0.5

                alpha = max(0, int(100 * (1 - distance / radius)))

                glow.set_at((x, y), (41, 255, 139, alpha))

        return glow