#!/usr/bin/python
import unittest

from main import *


class Test(unittest.TestCase):
    def test_sequence_combination(self):
        a = [1, 2, 3, 4]
        b = sequence_combination(a, 2)
        self.assertEqual(3, len(b))
        self.assertEqual([1, 2], b[0])
        self.assertEqual([2, 3], b[1])
        self.assertEqual([3, 4], b[2])

    def test_edge(self):
        edge1 = Edge(Point(1, 1), Point(1, -1))
        self.assertEqual(1, -edge1.C / edge1.A)

        edge2 = Edge(Point(1, 1), Point(-1, 1))
        self.assertEqual(1, -edge2.C / edge2.B)


if __name__ == '__main__':
    unittest.main()
