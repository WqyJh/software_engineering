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

        edge1 = Edge(Point(1, 1), Point(1, -1))
        edge2 = Edge(Point(1, -1), Point(-1, -1))
        edge3 = Edge(Point(-1, -1), Point(-1, 1))
        edge4 = Edge(Point(-1, 1), Point(1, 1))

        edges = [edge1, edge2, edge3, edge4]
        two_edge = sequence_combination(edges, 2)
        self.assertEqual(4, len(two_edge))
        self.assertEqual([edge1, edge2], two_edge[0])
        self.assertEqual([edge2, edge3], two_edge[1])
        self.assertEqual([edge3, edge4], two_edge[2])
        self.assertEqual([edge4, edge1], two_edge[3])


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

        edge2 = Edge(Point(1, 1), Point(-1, 1))
        (c3, c4) = nearest_two_circle(edge2, circles)
        self.assertEqual(c3, circle1)
        self.assertEqual(c4, circle4)

    def test_nearest_one_circle(self):
        edge1 = Edge(Point(1, 1), Point(1, -1))
        edge2 = Edge(Point(1, 1), Point(-1, 1))
        circle1 = Circle(0.5, 0.5, 0.5)
        circle2 = Circle(0.5, -0.5, 0.5)
        circle3 = Circle(-0.5, -0.5, 0.5)
        circle4 = Circle(-0.5, 0.5, 0.5)
        circles = (circle1, circle2, circle3, circle4)

        c = nearest_one_circle(edge1, edge2, circles)
        self.assertEqual(c, circle1)

        c1 = Circle(-0.5, 0.5, 1)
        c2 = Circle(0.5, -0.5, 0.9)
        c = nearest_one_circle(edge1, edge2, (c1, c2))
        self.assertEqual(c, c1)

    def test_eq(self):
        circle1 = Circle(0.5, 0.5, 0.5)
        circle2 = Circle(0.5, 0.5, 0.5)
        circle3 = Circle(0.5, 0.5, 0.6)
        self.assertTrue(circle1 == circle2)
        self.assertFalse(circle2 == circle3)

    def test_circle_exists(self):
        circle1 = Circle(0.5, 0.5, 0.5)
        circle2 = Circle(0.5, -0.5, 0.5)
        circle3 = Circle(-0.5, -0.5, 0.5)
        circle4 = Circle(-0.5, 0.5, 0.5)
        circles = (circle1, circle2, circle3)
        self.assertTrue(circle_exists(circles, circle1))
        self.assertTrue(circle_exists(circles, circle2))
        self.assertTrue(circle_exists(circles, circle3))
        self.assertFalse(circle_exists(circles, circle4))

if __name__ == '__main__':
    unittest.main()
