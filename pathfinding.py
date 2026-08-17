from collections import deque


class PathFinder:

    def __init__(self):
        self.directions = [
            (-1, 0),   # UP
            (1, 0),    # DOWN
            (0, -1),   # LEFT
            (0, 1)     # RIGHT
        ]

    def find_path(self, start, goal, obstacles, rows, cols):

        queue = deque()

        queue.append(start)

        visited = {start}

        parent = {}

        while queue:

            current = queue.popleft()

            # Goal reached
            if current == goal:
                return self.build_path(parent, start, goal)

            current_row, current_col = current

            for row_change, col_change in self.directions:

                next_row = current_row + row_change
                next_col = current_col + col_change

                next_position = (next_row, next_col)

                # Check grid boundaries
                if not (0 <= next_row < rows and
                        0 <= next_col < cols):
                    continue

                # Check obstacle
                if next_position in obstacles:
                    continue

                # Check already visited
                if next_position in visited:
                    continue

                visited.add(next_position)

                parent[next_position] = current

                queue.append(next_position)

        # No path found
        return []

    def build_path(self, parent, start, goal):

        path = []

        current = goal

        while current != start:

            path.append(current)

            current = parent[current]

        path.append(start)

        path.reverse()

        return path

    def get_next_position(self, start, goal, obstacles, rows, cols):

        path = self.find_path(
            start,
            goal,
            obstacles,
            rows,
            cols
        )

        if len(path) > 1:

            return path[1]

        return start