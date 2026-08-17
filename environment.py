import pygame
from settings import *

class Environment:

    def __init__(self):

        self.obstacles = [

            (1,2),
            (2,2),
            (4,1),
            (5,3)

        ]

    def draw(self,screen):

        for row in range(ROWS):

            for col in range(COLS):

                x = col * CELL_SIZE
                y = row * CELL_SIZE

                rect = pygame.Rect(
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(
                    screen,
                    LIGHT_BLUE,
                    rect
                )

                pygame.draw.rect(
                    screen,
                    BLACK,
                    rect,
                    2
                )

        for obstacle in self.obstacles:

            ox = obstacle[1] * CELL_SIZE
            oy = obstacle[0] * CELL_SIZE

            pygame.draw.rect(
                screen,
                GRAY,
                (
                    ox+15,
                    oy+15,
                    70,
                    70
                )
            )