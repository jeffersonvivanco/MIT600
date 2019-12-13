import unittest
from problem_solving_6.ps6 import *


class RectangularRoomTest(unittest.TestCase):
    def test_create(self):
        room = RectangularRoom(4, 4)
        self.assertEqual(0, room.get_num_cleaned_tiles())
        self.assertEqual(16, room.get_num_tiles())

    def test_clean(self):
        room = RectangularRoom(4, 4)
        pos = Position(0, 0)
        room.clean_tile_at_position(pos)
        self.assertTrue(room.is_tile_cleaned(0, 0))

        pos = Position(2.1, 3.2)
        room.clean_tile_at_position(pos)
        self.assertTrue(room.is_tile_cleaned(2, 3))

    def test_position(self):
        room = RectangularRoom(4, 4)
        pos = Position(3, 3)
        self.assertTrue(room.is_position_in_room(pos))

        pos = Position(4, 4)
        self.assertFalse(room.is_position_in_room(pos))

    def test_random_position(self):
        room = RectangularRoom(4, 4)
        self.assertIsNotNone(room.get_random_position())

    def test_get_new_position(self):
        pos = Position(3, 3)
        for _ in range(0, 100):
            print(pos)
            pos = pos.get_new_position(180, 1)
        self.assertTrue(True)


class RobotTest(unittest.TestCase):
    def test_create_robot(self):
        room = RectangularRoom(4, 4)
        robot = StandardRobot(room, 4)
        self.assertIsNotNone(robot)

    def test_update_position_and_clean(self):
        room = RectangularRoom(4, 4)
        robot = StandardRobot(room, 1)
        robot.update_position_and_clean()
        print(room)
        self.assertTrue(room.is_tile_cleaned(robot.get_robot_position().get_x(), robot.get_robot_position().get_y()))


if __name__ == '__main__':
    unittest.main()
