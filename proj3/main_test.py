#!/usr/bin/python
import unittest

from main import *


class Test(unittest.TestCase):
    def test_plane(self):
        plane1 = Plane(Point(1, 1, 1), Point(1, 1, -1), Point(1, -1, -1))
        self.assertEqual(1, -plane1.D / plane1.A)

        plane2 = Plane(Point(1, 1, 1), Point(1, -1, 1), Point(-1, 1, 1))
        self.assertEqual(1, -plane2.D / plane2.C)

    def test_eq(self):
        circle1 = Circle(0.5, 0.5, 0.5, 0.5)
        circle2 = Circle(0.5, 0.5, 0.5, 0.5)
        circle3 = Circle(0.5, 0.5, 0.5, 0.6)
        self.assertTrue(circle1 == circle2)
        self.assertFalse(circle2 == circle3)

    def test_circle_exists(self):
        circle1 = Circle(0.5, 0.5, 0.5, 0.5)
        circle2 = Circle(0.5, -0.5, 0.5, 0.5)
        circle3 = Circle(-0.5, -0.5, 0.5, 0.5)
        circle4 = Circle(-0.5, 0.5, 0.5, 0.5)
        circles = (circle1, circle2, circle3)
        self.assertTrue(circle_exists(circles, circle1))
        self.assertTrue(circle_exists(circles, circle2))
        self.assertTrue(circle_exists(circles, circle3))
        self.assertFalse(circle_exists(circles, circle4))

    def test_parallel_to(self):
        point1 = Point(1, 1, 1)
        point2 = Point(1, 1, -1)
        point3 = Point(1, -1, 1)
        point4 = Point(1, -1, -1)
        point5 = Point(-1, 1, 1)
        point6 = Point(-1, 1, -1)
        point7 = Point(-1, -1, 1)
        point8 = Point(-1, -1, -1)

        plane1 = Plane(point1, point2, point3)  # x = 1
        plane2 = Plane(point5, point6, point7)  # x = -1
        plane3 = Plane(point1, point2, point5)  # y = 1
        plane4 = Plane(point3, point4, point7)  # y = -1
        plane5 = Plane(point1, point3, point5)  # z = 1
        plane6 = Plane(point2, point4, point6)  # z = -1

        self.assertTrue(plane1.parallel_to(plane2))
        self.assertTrue(plane2.parallel_to(plane1))
        self.assertTrue(plane3.parallel_to(plane4))
        self.assertTrue(plane4.parallel_to(plane3))
        self.assertTrue(plane5.parallel_to(plane6))
        self.assertTrue(plane6.parallel_to(plane5))

        self.assertFalse(plane1.parallel_to(plane3))
        self.assertFalse(plane2.parallel_to(plane4))
        self.assertFalse(plane3.parallel_to(plane5))
        self.assertFalse(plane4.parallel_to(plane6))
        self.assertFalse(plane5.parallel_to(plane1))
        self.assertFalse(plane6.parallel_to(plane2))


if __name__ == '__main__':
    unittest.main()
