class Memory:

    def __init__(self):

        # Robot's current position
        self.robot_position = (0, 0)

        # Fire position
        self.fire_position = None

        # Obstacles known to the robot
        self.obstacles = []

        # Previous action performed by the robot
        self.previous_action = None

        # Whether fire has been detected
        self.fire_detected = False

        # Mission status
        self.mission_status = "Searching Fire"

    def update(self, robot_position, fire_position, obstacles):

        # Update current robot position
        self.robot_position = robot_position

        # Update fire information
        self.fire_position = fire_position

        # Remember obstacles
        self.obstacles = obstacles

        # Fire is detected if its position is known
        if fire_position is not None:
            self.fire_detected = True
        else:
            self.fire_detected = False

    def set_action(self, action):

        self.previous_action = action

    def set_status(self, status):

        self.mission_status = status