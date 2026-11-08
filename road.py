import pygame


class Road:
    def __init__(self):
        self.road_points = [
            (270, 150),
            (330, 150),
            (700, 800),
            (-100, 800)
        ]
        self.left_divider = [
            (290, 150),
            (166.67, 800)
        ]
        self.right_divider = [
            (310, 150),
            (433.34, 800)
        ]

        self.dash_progress = []

        for i in range(7):
            t = i / 7
            self.dash_progress.append(t)

    def update(self):
        for i in range(len(self.dash_progress)):
            self.dash_progress[i] = (self.dash_progress[i] + 0.005) % 1.0

    def interpolate_x(self, y, top, bottom):
        t = (y - top[1]) / (bottom[1] - top[1])
        x = top[0] + t * (bottom[0] - top[0])
        return x

    def get_perspective_scale(self, y):
        return (y - 150) / (800 - 150)

    def draw_road(self, screen):
        pygame.draw.polygon(screen, (82, 82, 82), self.road_points)
    
    def draw_left_divider(self, screen):
        for progress in self.dash_progress:
            y = 150 + (650) * (progress ** 2)
            scale = self.get_perspective_scale(y)
            dash_length = 10 + scale * 40
            half_length = dash_length / 2
            thickness = int(3 + scale * 8)

            y_start = y - half_length
            y_end = y + half_length

            y_start = max(150, min(800, y_start))
            y_end = max(150, min(800, y_end))

            x_start = self.interpolate_x(y_start, self.left_divider[0], self.left_divider[1])
            x_end = self.interpolate_x(y_end, self.left_divider[0], self.left_divider[1])

            pygame.draw.line(screen, (255, 255, 255), (x_start, y_start), (x_end, y_end), thickness)

    def draw_right_divider(self, screen):
        for progress in self.dash_progress:
            y = 150 + (650) * (progress ** 2)
            scale = self.get_perspective_scale(y)
            dash_length = 10 + scale * 40
            half_length = dash_length / 2
            thickness = int(3 + scale * 8)

            y_start = y - half_length
            y_end = y + half_length

            y_start = max(150, min(800, y_start))
            y_end = max(150, min(800, y_end))

            x_start = self.interpolate_x(y_start, self.right_divider[0], self.right_divider[1])
            x_end = self.interpolate_x(y_end, self.right_divider[0], self.right_divider[1])

            pygame.draw.line(screen, (255, 255, 255), (x_start, y_start), (x_end, y_end), thickness)