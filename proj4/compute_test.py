#!/usr/bin/env python3
import unittest

from compute import *


class Test(unittest.TestCase):
    def test_plane(self):
        plane1 = Plane(Point(1, 1, 1), Point(1, 1, -1), Point(1, -1, -1))
        self.assertEqual(1, -plane1.D / plane1.A)

        plane2 = Plane(Point(1, 1, 1), Point(1, -1, 1), Point(-1, 1, 1))
        self.assertEqual(1, -plane2.D / plane2.C)

    def test_eq(self):
        sphere1 = Sphere(0.5, 0.5, 0.5, 0.5)
        sphere2 = Sphere(0.5, 0.5, 0.5, 0.5)
        sphere3 = Sphere(0.5, 0.5, 0.5, 0.6)
        self.assertTrue(sphere1 == sphere2)
        self.assertFalse(sphere2 == sphere3)

    def test_sphere_exists(self):
        sphere1 = Sphere(0.5, 0.5, 0.5, 0.5)
        sphere2 = Sphere(0.5, -0.5, 0.5, 0.5)
        sphere3 = Sphere(-0.5, -0.5, 0.5, 0.5)
        sphere4 = Sphere(-0.5, 0.5, 0.5, 0.5)
        spheres = (sphere1, sphere2, sphere3)
        self.assertTrue(sphere_exists(spheres, sphere1))
        self.assertTrue(sphere_exists(spheres, sphere2))
        self.assertTrue(sphere_exists(spheres, sphere3))
        self.assertFalse(sphere_exists(spheres, sphere4))

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
