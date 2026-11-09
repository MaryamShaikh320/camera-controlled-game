import pygame

from road import Road


class Obstacle:
    def __init__(self, lane, road):
        self.lane = lane
        self.progress = 0
        self.road = road

    def update(self):
        self.progress = self.progress + 0.005

    def get_position(self):
        y = 150 + 650 * (self.progress**2)

        road_left_x = self.road.interpolate_x(
            y, self.road.road_points[0], self.road.road_points[3]
        )
        left_divider_x = self.road.interpolate_x(
            y, self.road.left_divider[0], self.road.left_divider[1]
        )
        right_divider_x = self.road.interpolate_x(
            y, self.road.right_divider[0], self.road.right_divider[1]
        )
        road_right_x = self.road.interpolate_x(
            y, self.road.road_points[1], self.road.road_points[2]
        )

        lane_centers = [
            (road_left_x + left_divider_x) / 2,
            (left_divider_x + right_divider_x) / 2,
            (right_divider_x + road_right_x) / 2,
        ]

        x = lane_centers[self.lane]

        return (x, y)

    def get_rect(self):
        width = 10 + self.progress * 80
        height = 5 + self.progress * 80

        x, y = self.get_position()

        rect_x = x - width / 2
        rect_y = y - height / 2

        return pygame.Rect(rect_x, rect_y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (222, 44, 44), self.get_rect())

    def is_at_player(self, player_y):
        player_progress = ((player_y - 150) / 650) ** 0.5

        return abs(self.progress - player_progress) < 0.025