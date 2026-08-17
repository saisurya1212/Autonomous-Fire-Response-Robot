class Sensor:

    def __init__(self, detection_range=6):
        self.detection_range = detection_range

    def detect_fire(self, robot, fire):

        if not fire.active:
            return False

        if fire.row is None or fire.col is None:
            return False

        row_distance = abs(robot.row - fire.row)
        col_distance = abs(robot.col - fire.col)

        distance = row_distance + col_distance

        return distance <= self.detection_range

    def scan(self, robot, fire, obstacles):

        fire_detected = self.detect_fire(robot, fire)

        return {
            "robot_position": (robot.row, robot.col),

            "fire_position": (
                (fire.row, fire.col)
                if fire.active
                else None
            ),

            "fire_detected": fire_detected,

            "obstacles": obstacles,

            "obstacle_count": len(obstacles)
        }