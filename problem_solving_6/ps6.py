import math, random


class Position:
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = round(x, 2)
        self.y = round(y, 2)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return '[position] x: {}, y: {}'.format(self.get_x(), self.get_y())

    def __repr__(self):
        return 'Position({}, {})'.format(self.x, self.y)


class RectangularRoom:
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        if width > 0 and height > 0:
            self.width = width
            self.height = height
            self.tiles = {} # '01': 'True'
        else:
            raise AppError('width and height must be > 0')

    def clean_tile_at_position(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles['{}{}'.format(int(pos.x), int(pos.y))] = True

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return '{}{}'.format(int(m), int(n)) in self.tiles.keys()

    def get_num_tiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def get_num_cleaned_tiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.tiles)

    def get_random_position(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        while True:
            x = random.random() * (self.width - 1)
            y = random.random() * (self.height - 1)
            pos = Position(x, y)
            if self.is_position_in_room(pos):
                return pos

    def is_position_in_room(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def __str__(self):
        return '[Room] tiles: {}, number of tiles: {}, number of tiles cleaned: {}'.format(self.tiles, self.get_num_tiles(),
                                                                                    self.get_num_cleaned_tiles())


class Robot:
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room: RectangularRoom, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.pos = room.get_random_position()
        self.direct = random.randint(0, 360)
        self.room.clean_tile_at_position(self.pos)

    def get_robot_position(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos

    def get_robot_direction(self):
        """
         Return the direction of the robot.

         returns: an integer d giving the direction of the robot as an angle in
         degrees, 0 <= d < 360.
         """
        return self.direct

    def set_position_robot(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direct = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError

    def __str__(self):
        return '[Robot] current pos: {}, current direction: {}'.format(self.pos, self.direct)


class StandardRobot(Robot):
    def __init__(self, room: RectangularRoom, speed):
        super().__init__(room, speed)

    def update_position_and_clean(self):
        new_pos = True
        while True:
            if new_pos:
                self.pos = self.pos.get_new_position(self.direct, self.speed)
            else:
                new_pos = True

            if self.room.is_position_in_room(self.pos):
                # print('pos {} in room, but not cleaned'.format(self.pos))
                if not self.room.is_tile_cleaned(self.pos.get_x(), self.pos.get_y()):
                    self.room.clean_tile_at_position(self.pos)
                    break
            else:
                # print('pos is not in room {}, getting random pos'.format(self.pos))
                self.pos = self.room.get_random_position()
                new_pos = False


class AppError(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


def run_simulation(num_robots, speed, width, height, min_coverage, num_trials, robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of time-steps needed to clean the fraction
    MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with speed SPEED, in a room with dimensions
    WIDTH x HEIGHT.
    """
    for _ in range(0, num_trials):
        robots = []
        room = RectangularRoom(width, height)
        for _ in range(0, num_robots):
            r = robot_type(room, speed)
            print(r)
            robots.append(r)
        clock_ticks = 0
        while round(len(room.tiles) / room.get_num_tiles(), 2) < min_coverage:
            clock_ticks +=1
            # print('clock tick: {}'.format(clock_ticks))
            for r in robots:
                r.update_position_and_clean()
                sorted(room.tiles)
                print(sorted(room.tiles))
                if round(len(room.tiles) / room.get_num_tiles(), 2) >= min_coverage:
                    break
        # print(room)


if __name__ == '__main__':
    run_simulation(1, 1, 4, 4, 1, 2, StandardRobot)