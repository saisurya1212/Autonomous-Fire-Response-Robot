import pygame
import math

from settings import (
    CELL_SIZE,
    GRID_X,
    GRID_Y
)


class Fire:

    def __init__(self):

        self.row = None
        self.col = None

        self.active = False
        self.extinguishing = False

        self.animation_time = 0

        self.water_timer = 0
        self.water_duration = 120

    def set_position(self, row, col):

        self.row = row
        self.col = col

        self.active = True
        self.extinguishing = False

        self.animation_time = 0
        self.water_timer = 0

    def start_extinguishing(self):

        if self.active:

            self.extinguishing = True
            self.water_timer = 0

    def update(self):

        if not self.active:
            return

        self.animation_time += 1

        if self.extinguishing:

            self.water_timer += 1

            if self.water_timer >= self.water_duration:

                self.active = False
                self.extinguishing = False

    def draw(self, screen):

        if not self.active:
            return

        # =================================
        # CORRECT GRID POSITION
        # =================================

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

        # =================================
        # FIRE
        # =================================

        if not self.extinguishing:

            font = pygame.font.SysFont(
                "Segoe UI Emoji",
                max(30, int(CELL_SIZE * 0.52))
            )

            # Small bouncing animation
            bounce = int(
                math.sin(
                    self.animation_time * 0.15
                ) * 4
            )

            fire_image = font.render(
                "🔥",
                True,
                (255, 255, 255)
            )

            rect = fire_image.get_rect(
                center=(x, y - bounce)
            )

            screen.blit(
                fire_image,
                rect
            )

        # =================================
        # EXTINGUISHING
        # =================================

        else:

            progress = (
                self.water_timer
                / self.water_duration
            )

            fire_size = int(
                CELL_SIZE * 0.52
                * (1 - progress)
            )

            if fire_size > 5:

                font = pygame.font.SysFont(
                    "Segoe UI Emoji",
                    fire_size
                )

                fire_image = font.render(
                    "🔥",
                    True,
                    (255, 255, 255)
                )

                rect = fire_image.get_rect(
                    center=(x, y)
                )

                screen.blit(
                    fire_image,
                    rect
                )

            # =================================
            # WATER STREAM
            # =================================

            pygame.draw.line(
                screen,
                (50, 150, 255),
                (
                    x,
                    y - CELL_SIZE * 0.70
                ),
                (
                    x,
                    y - CELL_SIZE * 0.20
                ),
                8
            )

            # =================================
            # WATER DROPLETS
            # =================================

            for i in range(7):

                drop_y = (
                    y
                    - CELL_SIZE * 0.65
                    + (
                        self.water_timer * 5
                        + i * 13
                    ) % int(CELL_SIZE * 0.65)
                )

                drop_x = (
                    x
                    + int(
                        math.sin(
                            self.water_timer * 0.15
                            + i
                        ) * 12
                    )
                )

                pygame.draw.circle(
                    screen,
                    (50, 150, 255),
                    (
                        drop_x,
                        drop_y
                    ),
                    4
                )