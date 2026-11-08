import pygame


class Player:
    def __init__(self):
        self.rect = pygame.Rect(280, 650, 40, 50)
        self.vertical_velocity = 0
        self.on_ground = True
        self.gravity = 1
        self.jump_velocity = -15
        self.current_lane = 1
        self.lane_positions = [80, 280, 480]

    def update(self, ground):
        self.vertical_velocity += self.gravity
        self.rect.y += self.vertical_velocity
        if self.rect.colliderect(ground) and self.vertical_velocity > 0:
            self.rect.bottom = ground.top
            self.vertical_velocity = 0
            self.on_ground = True

    def move_left(self):
        self.current_lane = max(0, self.current_lane - 1)
        self.rect.x = self.lane_positions[self.current_lane]
        print("Current lane:", self.current_lane)

    def move_right(self):
        self.current_lane = min(self.current_lane + 1, 2)
        self.rect.x = self.lane_positions[self.current_lane]
        print("Current lane:", self.current_lane)



    def jump(self, keys):
        if keys[pygame.K_UP] and self.on_ground:
            self.vertical_velocity = self.jump_velocity
            self.on_ground = False