#!/usr/bin/python
import unittest

from main import *


class Test(unittest.TestCase):
    def test_sequence_combination(self):
        a = [1, 2, 3, 4, 5]
        b = sequence_combination(a, 2)
        self.assertEqual(5, len(b))
        self.assertEqual([1, 2], b[0])
        self.assertEqual([2, 3], b[1])
        self.assertEqual([3, 4], b[2])
        self.assertEqual([4, 5], b[3])
        self.assertEqual([5, 1], b[4])

    def test_edge(self):
        edge1 = Edge(Point(1, 1), Point(1, -1))
        self.assertEqual(1, -edge1.C / edge1.A)

        edge2 = Edge(Point(1, 1), Point(-1, 1))
        self.assertEqual(1, -edge2.C / edge2.B)

    def test_nearest_two_circle(self):
        circle1 = Circle(0.5, 0.5, 0.5)
        circle2 = Circle(0.5, -0.5, 0.5)
        circle3 = Circle(-0.5, -0.5, 0.5)
        circle4 = Circle(-0.5, 0.5, 0.5)
        circles = (circle1, circle2, circle3, circle4)
        edge1 = Edge(Point(1, 1), Point(1, -1))
        (c1, c2) = nearest_two_circle(edge1, circles)
        self.assertEqual(c1, circle1)
        self.assertEqual(c2, circle2)

        edge2 = Edge(Point(1, 1), Point(-1,1))
        (c3, c4) = nearest_two_circle(edge2, circles)
        self.assertEqual(c3, circle1)
        self.assertEqual(c4, circle4)


if __name__ == '__main__':
    unittest.main()
