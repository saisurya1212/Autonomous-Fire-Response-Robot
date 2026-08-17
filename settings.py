import pygame

pygame.init()

# ==========================================
# FULL SCREEN
# ==========================================

screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption(
    "Autonomous Fire Response Robot"
)


# ==========================================
# GRID
# ==========================================

ROWS = 6
COLS = 6

GRID_SIZE = int(HEIGHT * 0.82)

CELL_SIZE = GRID_SIZE // COLS

# Position of grid on full screen
GRID_X = 40
GRID_Y = (HEIGHT - GRID_SIZE) // 2


# ==========================================
# COLORS
# ==========================================

WHITE = (255, 255, 255)

BLACK = (40, 40, 40)

LIGHT_BLUE = (220, 235, 255)

GRAY = (120, 120, 120)

GREEN = (0, 180, 0)

RED = (255, 0, 0)

DARK_GREEN = (0, 120, 0)

YELLOW = (255, 220, 0)

ORANGE = (255, 140, 0)