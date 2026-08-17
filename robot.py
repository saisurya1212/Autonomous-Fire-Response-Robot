import pygame

from settings import (
    CELL_SIZE,
    GRID_X,
    GRID_Y
)


class Robot:

    def __init__(self):

        self.row = 0
        self.col = 0

        # Base position
        self.base_row = 0
        self.base_col = 0

    def set_position(self, row, col):

        self.row = row
        self.col = col

    def at_base(self):

        return (
            self.row == self.base_row
            and self.col == self.base_col
        )

    def draw(self, screen):

        # Correct grid coordinates
        x = (
            GRID_X
            + self.col * CELL_SIZE
            + CELL_SIZE // 2
        )

        y = (
            GRID_Y
            + self.row * CELL_SIZE
            + CELL_SIZE // 2
        )

        # Robot emoji
        try:

            font = pygame.font.SysFont(
                "Segoe UI Emoji",
                max(30, int(CELL_SIZE * 0.52))
            )

            robot_image = font.render(
                "🤖",
                True,
                (0, 0, 0)
            )

            rect = robot_image.get_rect(
                center=(x, y)
            )

            screen.blit(
                robot_image,
                rect
            )

        except:

            pygame.draw.circle(
                screen,
                (0, 180, 0),
                (x, y),
                int(CELL_SIZE * 0.25)
            )