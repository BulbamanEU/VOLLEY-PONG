import unittest
from unittest.mock import MagicMock, patch
import pygame
from main import *

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_choose_strength_short_hold(self):
        time = 0.3
        expected_strength = 0

        actual_strength = choose_strength(time)

        self.assertEqual(expected_strength, actual_strength)

    def test_choose_strength_long_hold(self):
        time = 5
        expected_strength = 3

        actual_strength = choose_strength(time)

        self.assertEqual(expected_strength, actual_strength)

    def test_ending_x(self):
        test_starting_x = 125
        test_starting_y = 85
        test_angle = 45
        test_speed = 10
        gravity = 10
        end_y = 85
        expected_ending_x = 135

        actual_ending_x = calculate_ending_x(test_starting_x,test_starting_y, test_angle, test_speed, gravity, end_y)
        self.assertEqual(expected_ending_x, actual_ending_x)

    def test_right_wall(self):
        test_ball_x = SCREEN_WIDTH - 20
        test_travel_x = 60
        test_invert = False
        value0, test_invert, value1 = wall_touch(test_ball_x, test_invert, test_travel_x, SCREEN_WIDTH)
        self.assertEqual(True, test_invert)

    def test_left_wall(self):
        test_ball_x = 20
        test_travel_x = - 60
        test_invert = False
        value0, test_invert, value1 = wall_touch(test_ball_x, test_invert, test_travel_x, SCREEN_WIDTH)
        self.assertEqual(True, test_invert)




if __name__ == '__main__':
    unittest.main()
