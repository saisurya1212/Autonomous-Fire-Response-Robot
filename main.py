import pygame
import sys
from collections import deque

from robot import Robot
from fire import Fire
from sensor import Sensor

from settings import (
    screen,
    WIDTH,
    HEIGHT,
    ROWS,
    COLS,
    GRID_SIZE,
    CELL_SIZE,
    WHITE,
    BLACK,
    LIGHT_BLUE,
    GRAY,
    GREEN,
    RED,
    DARK_GREEN,
    YELLOW
)


# ==========================================
# INITIALIZATION
# ==========================================

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption(
    "Autonomous Fire Response Robot"
)


# ==========================================
# GRID POSITION
# ==========================================

GRID_X = 40
GRID_Y = (HEIGHT - GRID_SIZE) // 2


# ==========================================
# OBJECTS
# ==========================================

robot = Robot()

# Multiple fires
fires = []

sensor = Sensor()


# ==========================================
# OBSTACLES
# ==========================================

obstacles = [
    (1, 2),
    (2, 4),
    (4, 1),
    (5, 3),
    (0, 5)
]


# ==========================================
# AGENT STATE
# ==========================================

mode = "WAITING"

battery = 100

path = []
path_index = 0

move_timer = 0
move_delay = 20

charging_timer = 0

# Current fire robot is handling
target_fire = None


# ==========================================
# FONTS
# ==========================================

font = pygame.font.SysFont(
    "Arial",
    20
)

small_font = pygame.font.SysFont(
    "Arial",
    17
)

big_font = pygame.font.SysFont(
    "Arial",
    28
)

title_font = pygame.font.SysFont(
    "Arial",
    30,
    bold=True
)


# ==========================================
# PATHFINDING
# ==========================================

def find_path(start, goal):

    queue = deque()

    queue.append(start)

    visited = set()
    visited.add(start)

    parent = {}

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:

        current = queue.popleft()

        if current == goal:

            result = []

            node = goal

            while node != start:

                result.append(node)
                node = parent[node]

            result.append(start)

            result.reverse()

            return result

        for dr, dc in directions:

            nr = current[0] + dr
            nc = current[1] + dc

            next_cell = (nr, nc)

            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue

            if next_cell in obstacles:
                continue

            if next_cell in visited:
                continue

            visited.add(next_cell)

            parent[next_cell] = current

            queue.append(next_cell)

    return []


# ==========================================
# GET ACTIVE FIRES
# ==========================================

def get_active_fires():

    return [
        fire for fire in fires
        if fire.active
    ]


# ==========================================
# SELECT NEXT FIRE
# ==========================================

def select_next_fire():

    global target_fire
    global path
    global path_index
    global mode

    active_fires = get_active_fires()

    if not active_fires:

        target_fire = None

        return False

    # Choose nearest fire using Manhattan distance
    target_fire = min(
        active_fires,
        key=lambda fire:
        abs(robot.row - fire.row)
        +
        abs(robot.col - fire.col)
    )

    path = find_path(
        (robot.row, robot.col),
        (target_fire.row, target_fire.col)
    )

    path_index = 0

    if path:

        mode = "SEARCHING"

        return True

    # If selected fire has no path,
    # try another fire
    for fire in active_fires:

        test_path = find_path(
            (robot.row, robot.col),
            (fire.row, fire.col)
        )

        if test_path:

            target_fire = fire
            path = test_path
            path_index = 0
            mode = "SEARCHING"

            return True

    target_fire = None

    return False


# ==========================================
# PLACE FIRE
# ==========================================

def place_fire(row, col):

    global mode

    # Cannot place fire on obstacle
    if (row, col) in obstacles:
        return

    # Cannot place fire on base
    if (row, col) == (0, 0):
        return

    # Cannot place fire on robot
    if (row, col) == (robot.row, robot.col):
        return

    # Prevent duplicate fire in same cell
    for fire in fires:

        if (
            fire.active
            and
            fire.row == row
            and
            fire.col == col
        ):

            return

    # Create new fire
    new_fire = Fire()

    new_fire.set_position(
        row,
        col
    )

    fires.append(new_fire)

    # If robot is waiting or mission was complete,
    # immediately start handling the new fire
    if mode in [
        "WAITING",
        "MISSION COMPLETE"
    ]:

        select_next_fire()


# ==========================================
# DRAW TEXT HELPER
# ==========================================

def draw_text(
    text,
    x,
    y,
    font_object=font,
    color=BLACK
):

    surface = font_object.render(
        text,
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


# ==========================================
# DRAW GRID
# ==========================================

def draw_grid():

    for row in range(ROWS):

        for col in range(COLS):

            x = GRID_X + col * CELL_SIZE
            y = GRID_Y + row * CELL_SIZE

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


# ==========================================
# DRAW BASE
# ==========================================

def draw_base():

    base_rect = pygame.Rect(
        GRID_X + 5,
        GRID_Y + 5,
        CELL_SIZE - 10,
        CELL_SIZE - 10
    )

    pygame.draw.rect(
        screen,
        (200, 255, 200),
        base_rect
    )

    base_font = pygame.font.SysFont(
        "Segoe UI Emoji",
        25
    )

    base_text = base_font.render(
        "🏠",
        True,
        BLACK
    )

    screen.blit(
        base_text,
        base_text.get_rect(
            center=(
                GRID_X + CELL_SIZE // 2,
                GRID_Y + CELL_SIZE // 2
            )
        )
    )


# ==========================================
# DRAW OBSTACLES
# ==========================================

def draw_obstacles():

    for row, col in obstacles:

        x = GRID_X + col * CELL_SIZE
        y = GRID_Y + row * CELL_SIZE

        pygame.draw.rect(
            screen,
            GRAY,
            (
                x + 15,
                y + 15,
                CELL_SIZE - 30,
                CELL_SIZE - 30
            )
        )


# ==========================================
# DRAW PANEL
# ==========================================

def draw_panel():

    panel_x = GRID_X + GRID_SIZE + 35

    panel_width = WIDTH - panel_x - 30

    panel_rect = pygame.Rect(
        panel_x - 15,
        20,
        panel_width + 15,
        HEIGHT - 40
    )

    pygame.draw.rect(
        screen,
        (245, 248, 252),
        panel_rect
    )

    pygame.draw.rect(
        screen,
        (180, 190, 200),
        panel_rect,
        2
    )

    # --------------------------------------
    # TITLE
    # --------------------------------------

    draw_text(
        "AUTONOMOUS",
        panel_x,
        45,
        title_font,
        BLACK
    )

    draw_text(
        "FIRE RESPONSE ROBOT",
        panel_x,
        82,
        title_font,
        BLACK
    )

    # --------------------------------------
    # ROBOT STATUS
    # --------------------------------------

    draw_text(
        "ROBOT STATUS",
        panel_x,
        145,
        font,
        DARK_GREEN
    )

    draw_text(
        f"Position : ({robot.row}, {robot.col})",
        panel_x,
        180
    )

    draw_text(
        f"Mode : {mode}",
        panel_x,
        210
    )

    # --------------------------------------
    # FIRE STATUS
    # --------------------------------------

    draw_text(
        "FIRE STATUS",
        panel_x,
        260,
        font,
        RED
    )

    active_fires = get_active_fires()

    draw_text(
        f"Active Fires : {len(active_fires)}",
        panel_x,
        295,
        color=RED if active_fires else BLACK
    )

    if target_fire is not None:

        draw_text(
            f"Target : ({target_fire.row}, {target_fire.col})",
            panel_x,
            325
        )

    else:

        draw_text(
            "Target : None",
            panel_x,
            325
        )

    # --------------------------------------
    # BATTERY
    # --------------------------------------

    draw_text(
        "BATTERY",
        panel_x,
        375,
        font,
        DARK_GREEN
    )

    draw_text(
        f"{battery}%",
        panel_x,
        410,
        big_font,
        DARK_GREEN
    )

    # Battery bar

    bar_x = panel_x
    bar_y = 450

    bar_width = max(
        100,
        panel_width - 20
    )

    bar_height = 18

    pygame.draw.rect(
        screen,
        GRAY,
        (
            bar_x,
            bar_y,
            bar_width,
            bar_height
        )
    )

    fill_width = int(
        bar_width * battery / 100
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (
            bar_x,
            bar_y,
            fill_width,
            bar_height
        )
    )

    # --------------------------------------
    # AGENT MEMORY
    # --------------------------------------

    draw_text(
        "AGENT MEMORY",
        panel_x,
        500,
        font,
        BLACK
    )

    detected = "YES" if active_fires else "NO"

    draw_text(
        f"Fire Detected : {detected}",
        panel_x,
        530,
        small_font
    )

    draw_text(
        f"Obstacles : {len(obstacles)}",
        panel_x,
        555,
        small_font
    )

    # --------------------------------------
    # CURRENT ACTION
    # --------------------------------------

    action_y = 590

    if mode == "SEARCHING":

        action = "Moving to Fire"

    elif mode == "EXTINGUISHING":

        action = "Extinguishing Fire"

    elif mode == "RETURNING":

        action = "Returning to Base"

    elif mode == "CHARGING":

        action = "Charging"

    elif mode == "MISSION COMPLETE":

        action = "Mission Complete"

    else:

        action = "Waiting for Fire"

    draw_text(
        f"Action : {action}",
        panel_x,
        action_y,
        small_font,
        BLACK
    )


# ==========================================
# MAIN LOOP
# ==========================================

running = True

while running:

    # ======================================
    # EVENTS
    # ======================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ----------------------------------
        # ESC → EXIT
        # ----------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

        # ----------------------------------
        # MOUSE → PLACE FIRE
        # ----------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check whether click is inside grid
            if (
                GRID_X <= mouse_x < GRID_X + GRID_SIZE
                and
                GRID_Y <= mouse_y < GRID_Y + GRID_SIZE
            ):

                col = (
                    mouse_x - GRID_X
                ) // CELL_SIZE

                row = (
                    mouse_y - GRID_Y
                ) // CELL_SIZE

                place_fire(
                    row,
                    col
                )

    # ======================================
    # SENSOR
    # ======================================

    if target_fire is not None:

        perception = sensor.scan(
            robot,
            target_fire,
            obstacles
        )

    else:

        perception = None

    # ======================================
    # FIRE ANIMATION
    # ======================================

    for fire in fires:

        fire.update()

    # ======================================
    # SEARCHING
    # ======================================

    if mode == "SEARCHING":

        # If current target disappeared,
        # select another fire
        if (
            target_fire is None
            or
            not target_fire.active
        ):

            if not select_next_fire():

                path = find_path(
                    (robot.row, robot.col),
                    (0, 0)
                )

                path_index = 0

                mode = "RETURNING"

        else:

            move_timer += 1

            if move_timer >= move_delay:

                move_timer = 0

                if path_index < len(path) - 1:

                    path_index += 1

                    next_row, next_col = path[path_index]

                    robot.set_position(
                        next_row,
                        next_col
                    )

                    battery = max(
                        0,
                        battery - 1
                    )

                else:

                    mode = "EXTINGUISHING"

                    target_fire.start_extinguishing()

    # ======================================
    # EXTINGUISHING
    # ======================================

    elif mode == "EXTINGUISHING":

        # Wait until current fire is extinguished
        if (
            target_fire is not None
            and
            not target_fire.active
        ):

            # Check for remaining fires
            remaining_fires = get_active_fires()

            if remaining_fires:

                # Go directly to next fire
                select_next_fire()

            else:

                # All fires extinguished
                target_fire = None

                path = find_path(
                    (robot.row, robot.col),
                    (0, 0)
                )

                path_index = 0

                mode = "RETURNING"

    # ======================================
    # RETURNING
    # ======================================

    elif mode == "RETURNING":

        # If a new fire appears while returning,
        # handle it instead of continuing to base
        if get_active_fires():

            select_next_fire()

        else:

            move_timer += 1

            if move_timer >= move_delay:

                move_timer = 0

                if path_index < len(path) - 1:

                    path_index += 1

                    next_row, next_col = path[path_index]

                    robot.set_position(
                        next_row,
                        next_col
                    )

                    battery = max(
                        0,
                        battery - 1
                    )

                else:

                    mode = "CHARGING"

                    charging_timer = 0

    # ======================================
    # CHARGING
    # ======================================

    elif mode == "CHARGING":

        # If a new fire is created while charging,
        # stop charging and respond
        if get_active_fires():

            select_next_fire()

        else:

            charging_timer += 1

            if charging_timer >= 5:

                charging_timer = 0

                battery += 1

                if battery >= 100:

                    battery = 100

                    mode = "MISSION COMPLETE"

    # ======================================
    # MISSION COMPLETE
    # ======================================

    elif mode == "MISSION COMPLETE":

        # If a new fire appears after mission completion
        if get_active_fires():

            select_next_fire()

    # ======================================
    # DRAW
    # ======================================

    screen.fill(WHITE)

    draw_grid()

    draw_base()

    draw_obstacles()

    # Draw ALL fires
    for fire in fires:

        fire.draw(screen)

    # Draw robot
    robot.draw(
        screen
    )

    # Draw information panel
    draw_panel()

    # ======================================
    # UPDATE DISPLAY
    # ======================================

    pygame.display.flip()

    clock.tick(60)


# ==========================================
# EXIT
# ==========================================

pygame.quit()

sys.exit()