#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
from scipy.optimize import fsolve
from math import sqrt
import itertools
import threading
import threadpool

from ivisual import *

EPSINON = 1e-6


def float_equals(f1, f2):
    return abs(f1 - f2) < EPSINON


def float_lt(f1, f2):
    if not float_equals(f1, f2):
        return f1 < f2
    return False


class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Circle(object):
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def intersect_with(self, circle):
        d1 = pow(self.x - circle.x, 2) + pow(self.y - circle.y, 2) + pow(self.z - circle.z, 2)
        d2 = pow(self.r + circle.r, 2)
        if not float_equals(d1, d2):
            return d1 < d2
        return False

    def equals(self, other):
        return float_equals(self.x, other.x) and float_equals(self.y, other.y) \
               and float_equals(self.z, other.z) and float_equals(self.r, other.r)

    def __eq__(self, other):
        return float_equals(self.r, other.r)

    def __lt__(self, other):
        return float_lt(self.r, other.r)


class Plane(object):
    def __init__(self, point1, point2, point3):
        x1, y1, z1 = point1.x, point1.y, point1.z
        x2, y2, z2 = point2.x, point2.y, point2.z
        x3, y3, z3 = point3.x, point3.y, point3.z
        self.A = (y2 - y1) * (z3 - z1) - (y3 - y1) * (z2 - z1)
        self.B = (z2 - z1) * (x3 - x1) - (z3 - z1) * (x2 - x1)
        self.C = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
        self.D = -self.A * x1 - self.B * y1 - self.C * z1

    def dist_to_point(self, x, y, z):
        return abs(self.A * x + self.B * y + self.C * z + self.D) / \
               sqrt(self.A * self.A + self.B * self.B + self.C * self.C)

    def parallel_to(self, other):
        return float_equals(1, abs(self.A * other.A + self.B * other.B + self.C * other.C) / \
                            (sqrt(self.A * self.A + self.B * self.B + self.C * self.C) * \
                             sqrt(other.A * other.A + other.B * other.B + other.C * other.C)))


def plane_A_neq_0(planes):
    for plane in planes:
        if plane.A != 0:
            return plane


def plane_B_neq_0(planes):
    for plane in planes:
        if plane.B != 0:
            return plane


def plane_C_neq_0(planes):
    for plane in planes:
        if plane.C != 0:
            return plane


def one_circle_three_plane(circle1, plane1, plane2, plane3):
    x1, y1, z1, r1 = circle1.x, circle1.y, circle1.z, circle1.r
    planes = [plane1, plane2, plane3]
    plane1, plane2, plane3 = plane_A_neq_0(planes), plane_B_neq_0(planes), plane_C_neq_0(planes)
    x2 = -plane1.D / plane1.A
    y3 = -plane2.D / plane2.B
    z4 = -plane3.D / plane3.C
    x0 = (x1 + x2) / 2
    y0 = (y1 + y3) / 2
    z0 = (z1 + z4) / 2
    r0 = min(plane1.dist_to_point(x0, y0, z0), plane2.dist_to_point(x0, y0, z0), plane3.dist_to_point(x0, y0, z0))

    def equations(p):
        x, y, z, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                plane1.dist_to_point(x, y, z) - r,
                plane2.dist_to_point(x, y, z) - r,
                plane3.dist_to_point(x, y, z) - r)

    x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
    return Circle(x, y, z, r)


def two_circle_two_plane(circle1, circle2, plane1, plane2):
    x1, y1, z1, r1 = circle1.x, circle1.y, circle1.z, circle1.r
    x2, y2, z2, r2 = circle2.x, circle2.y, circle2.z, circle2.r

    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2
    z0 = (z1 + z2) / 2

    if plane1.A != 0:
        x3 = -plane1.D / plane1.A
        x0 = (x0 + x3) / 2
    elif plane1.B != 0:
        y3 = -plane1.D / plane1.B
        y0 = (y0 + y3) / 2
    elif plane1.C != 0:
        z3 = -plane1.D / plane1.C
        z0 = (z0 + z3) / 2

    if plane2.A != 0:
        x3 = -plane2.D / plane2.A
        x0 = (x0 + x3) / 2
    elif plane2.B != 0:
        y3 = -plane2.D / plane2.B
        y0 = (y0 + y3) / 2
    elif plane2.C != 0:
        z3 = -plane2.D / plane2.C
        z0 = (z0 + z3) / 2

    r0 = min(plane1.dist_to_point(x0, y0, z0), plane2.dist_to_point(x0, y0, z0))

    def equations(p):
        x, y, z, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                pow(x - x2, 2) + pow(y - y2, 2) + pow(z - z2, 2) - pow(r + r2, 2),
                plane1.dist_to_point(x, y, z) - r,
                plane2.dist_to_point(x, y, z) - r)

    x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
    return Circle(x, y, z, r)


def three_circle(circle1, circle2, circle3):
    x1, y1, r1 = circle1.x, circle1.y, circle1.r
    x2, y2, r2 = circle2.x, circle2.y, circle2.r
    x3, y3, r3 = circle3.x, circle3.y, circle3.r

    def equations(p):
        x, y, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) - pow(r + r1, 2),
                pow(x - x2, 2) + pow(y - y2, 2) - pow(r + r2, 2),
                pow(x - x3, 2) + pow(y - y3, 2) - pow(r + r3, 2))

    c1, c2, c3 = circle1, circle2, circle3
    # 将 c1, c2, c3 从小到大排列
    if c1.r > c2.r:
        c1, c2 = c2, c1
    if c2.r > c3.r:
        c2, c3 = c3, c2

    ((x, y, r), info, status, mesg) = fsolve(equations, (((c1.x + c2.x) / 2), (c1.y + c2.y) / 2, (c1.r + c2.r) / 2), \
                                             full_output=True)
    if status == 1:
        return Circle(x, y, r)
    else:
        return Circle(0, 0, 0)


def three_circle_one_plane(circle1, circle2, circle3, plane):
    x1, y1, z1, r1 = circle1.x, circle1.y, circle1.z, circle1.r
    x2, y2, z2, r2 = circle2.x, circle2.y, circle2.z, circle2.r
    x3, y3, z3, r3 = circle3.x, circle3.y, circle3.z, circle3.r

    x0 = (x1 + x2 + x3) / 3
    y0 = (y1 + y2 + y3) / 3
    z0 = (z1 + z2 + z3) / 3
    if plane.A != 0:
        x4 = -plane.D / plane.A
        x0 = (x0 + x4) / 2
    elif plane.B != 0:
        y4 = -plane.D / plane.B
        y0 = (y0 + y4) / 2
    elif plane.C != 0:
        z4 = -plane.D / plane.C
        z0 = (z0 + z4) / 2

    r0 = plane.dist_to_point(x0, y0, z0)

    def equations(p):
        x, y, z, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                pow(x - x2, 2) + pow(y - y2, 2) + pow(z - z2, 2) - pow(r + r2, 2),
                pow(x - x3, 2) + pow(y - y3, 2) + pow(z - z3, 2) - pow(r + r3, 2),
                plane.dist_to_point(x, y, z) - r)

    x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
    return Circle(x, y, z, r)


def four_circle(circle1, circle2, circle3, circle4):
    circle1, circle2, circle3, circle4 = sorted([circle1, circle2, circle3, circle4])

    x1, y1, z1, r1 = circle1.x, circle1.y, circle1.z, circle1.r
    x2, y2, z2, r2 = circle2.x, circle2.y, circle2.z, circle2.r
    x3, y3, z3, r3 = circle3.x, circle3.y, circle3.z, circle3.r
    x4, y4, z4, r4 = circle4.x, circle4.y, circle4.z, circle4.r

    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2
    z0 = (z1 + z2) / 2
    r0 = (r1 + r2) / 2

    def equations(p):
        x, y, z, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                pow(x - x2, 2) + pow(y - y2, 2) + pow(z - z2, 2) - pow(r + r2, 2),
                pow(x - x3, 2) + pow(y - y3, 2) + pow(z - z3, 2) - pow(r + r3, 2),
                pow(x - x4, 2) + pow(y - y4, 2) + pow(z - z4, 2) - pow(r + r4, 2))

    x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
    return Circle(x, y, z, r)


def circle_filter(circles):
    """
    过滤出半径大于0的圆
    :param circles:
    :return:
    """
    list = []
    for circle in circles:
        if circle.r > 0:
            list.append(circle)
    return list


class Area(object):
    def __init__(self, atype, planes, circles):
        self.atype = atype
        self.planes = planes
        self.circles = circles
        self.in_circle = None

    class Type(object):
        ONE_CIRCLE_THREE_PLANE = 0
        TWO_CIRCLE_TWO_PLANE = 1
        THREE_CIRCLE_ONE_PLANE = 2
        FOUR_CIRCLE = 3

    def inner_circle(self):
        if self.in_circle is None:
            if self.atype == Area.Type.ONE_CIRCLE_THREE_PLANE:
                self.in_circle = one_circle_three_plane(self.circles[0], self.planes[0], self.planes[1], self.planes[2])
            elif self.atype == Area.Type.TWO_CIRCLE_TWO_PLANE:
                self.in_circle = two_circle_two_plane(self.circles[0], self.circles[1], self.planes[0], self.planes[1])
            elif self.atype == Area.Type.THREE_CIRCLE_ONE_PLANE:
                self.in_circle = three_circle_one_plane(self.circles[0], self.circles[1], self.circles[2],
                                                        self.planes[0])
            elif self.atype == Area.Type.FOUR_CIRCLE:
                self.in_circle = four_circle(self.circles[0], self.circles[1], self.circles[2], self.circles[3])
        return self.in_circle

    def new_areas(self, inner_circle):
        if self.atype == Area.Type.ONE_CIRCLE_THREE_PLANE:
            # if self.circles[0].r == 0:
            #     return [Area(Area.Type.ONE_CIRCLE_THREE_PLANE, self.planes, [inner_circle, ])]
            return [Area(Area.Type.ONE_CIRCLE_THREE_PLANE, self.planes, [inner_circle, ]),
                    Area(Area.Type.TWO_CIRCLE_TWO_PLANE, [self.planes[0], self.planes[1]],
                         [self.circles[0], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_TWO_PLANE, [self.planes[0], self.planes[2]],
                         [self.circles[0], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_TWO_PLANE, [self.planes[1], self.planes[2]],
                         [self.circles[0], inner_circle])]
        elif self.atype == Area.Type.TWO_CIRCLE_TWO_PLANE:
            # if self.circles[0].r == 0 and self.circles[1].r == 0:
            #     return []
            # elif self.circles[0].r == 0 or self.circles[1].r == 0:
            #     c = self.circles[0] if self.circles[0].r != 0 else self.circles[1]
            #     return [Area(Area.Type.TWO_CIRCLE_TWO_PLANE, self.planes, [inner_circle, c])]
            return [Area(Area.Type.TWO_CIRCLE_TWO_PLANE, self.planes, [self.circles[0], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_TWO_PLANE, self.planes, [self.circles[1], inner_circle]),
                    Area(Area.Type.THREE_CIRCLE_ONE_PLANE, self.planes[0],
                         [self.circles[0], self.circles[1], inner_circle]),
                    Area(Area.Type.THREE_CIRCLE_ONE_PLANE, self.planes[1],
                         [self.circles[0], self.circles[1], inner_circle])]
        elif self.atype == Area.Type.FOUR_CIRCLE:
            # filtered_circle = circle_filter(self.circles)
            # if len(filtered_circle) == 0 or len(filtered_circle) == 1:
            #     return []
            # elif len(filtered_circle) == 2:
            #     return [Area(Area.Type.FOUR_CIRCLE, [], [filtered_circle[0], filtered_circle[1], inner_circle])]
            return [Area(Area.Type.FOUR_CIRCLE, [], [self.circles[0], self.circles[1], self.circles[2], inner_circle]),
                    Area(Area.Type.FOUR_CIRCLE, [], [self.circles[0], self.circles[1], self.circles[3], inner_circle]),
                    Area(Area.Type.FOUR_CIRCLE, [], [self.circles[0], self.circles[2], self.circles[3], inner_circle]),
                    Area(Area.Type.FOUR_CIRCLE, [], [self.circles[1], self.circles[2], self.circles[3], inner_circle])]


# 检查 area 是否合法
def check_area(area, circles, planes):
    circle = area.inner_circle()
    for c in circles:
        if circle.intersect_with(c):
            return False
    for plane in planes:
        if float_lt(plane.dist_to_point(circle.x, circle.y, circle.z), circle.r):
            return False
    return True


def circle_exists(circles, circle):
    for c in circles:
        if c.equals(circle):
            return True
    return False


def plot(result, blocks, name):
    scene = canvas(title='3D scene')

    for block in blocks:
        sphere(pos=vector(block.x, block.y, block.z), radius=1.0 / 50, color=color.red)

    for circle in result:
        sphere(pos=vector(circle.x, circle.y, circle.z), radius=circle.r, color=color.blue)

    box(pos=vector(0, 0, 0), size=(2, 2, 2), color=color.blue, opacity=0.2)


def sumr2(result):
    s = 0
    for circle in result:
        s += circle.r * circle.r
    return s


def block_filter(blocks, planes):
    """
    过滤掉无效的障碍。在边界上的障碍为无效障碍
    :param blocks:
    :return:
    """
    for block in blocks:
        for plane in planes:
            if float_equals(0, plane.dist_to_point(block.x, block.y, block.z)):
                blocks.remove(block)
    return blocks


def compute_four_circle(circles, planes, output):
    max_circle_area = None
    max_circle = Circle(0, 0, 0, 0)
    for four_circle in itertools.combinations(circles, 4):
        area = Area(Area.Type.FOUR_CIRCLE, [], four_circle)
        if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
            max_circle_area = area
            max_circle = area.inner_circle()
    output.append((max_circle_area, max_circle))


def compute_three_circle_one_plane(circles, planes, output):
    max_circle_area = None
    max_circle = Circle(0, 0, 0, 0)
    for plane in planes:
        three_circles = itertools.combinations(circles, 3)
        for three_circle in three_circles:
            area = Area(Area.Type.THREE_CIRCLE_ONE_PLANE, [plane, ], three_circle)
            if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
                max_circle_area = area
                max_circle = area.inner_circle()
    output.append((max_circle_area, max_circle))


def compute_two_circle_two_plane(circles, planes, output):
    max_circle_area = None
    max_circle = Circle(0, 0, 0, 0)
    for two_plane in itertools.combinations(planes, 2):
        if not two_plane[0].parallel_to(two_plane[1]):
            two_circles = itertools.combinations(circles, 2)
            for two_circle in two_circles:
                area = Area(Area.Type.TWO_CIRCLE_TWO_PLANE, two_plane, two_circle)
                if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
                    max_circle_area = area
                    max_circle = area.inner_circle()
    output.append((max_circle_area, max_circle))


def compute_one_circle_three_plane(circles, planes, output):
    max_circle_area = None
    max_circle = Circle(0, 0, 0, 0)
    for three_plane in itertools.combinations(planes, 3):
        if not three_plane[0].parallel_to(three_plane[1]) and \
                not three_plane[1].parallel_to(three_plane[2]) and \
                not three_plane[2].parallel_to(three_plane[0]):
            for circle in circles:
                area = Area(Area.Type.ONE_CIRCLE_THREE_PLANE, three_plane, [circle, ])
                if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
                    max_circle_area = area
                    max_circle = area.inner_circle()
    output.append((max_circle_area, max_circle))


def main(m, blocks):
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

    planes = [plane1, plane2, plane3, plane4, plane5, plane6]

    block_filter(blocks, planes)

    circles = [] + blocks

    output = []
    while m > 0:
        max_circle_area = None
        max_circle = Circle(0, 0, 0, 0)

        output.clear()
        compute_four_circle(circles, planes, output)
        compute_three_circle_one_plane(circles, planes, output)
        compute_two_circle_two_plane(circles, planes, output)
        compute_one_circle_three_plane(circles, planes, output)

        for (m_c_a, m_c) in output:
            if m_c.r > max_circle.r:
                max_circle_area = m_c_a
                max_circle = m_c

        # # 四个圆
        # for four_circle in itertools.combinations(circles, 4):
        #     area = Area(Area.Type.FOUR_CIRCLE, [], four_circle)
        #     if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
        #         max_circle_area = area
        #         max_circle = area.inner_circle()
        #
        # # 一个面，三个圆
        # for plane in planes:
        #     three_circles = itertools.combinations(circles, 3)
        #     for three_circle in three_circles:
        #         area = Area(Area.Type.THREE_CIRCLE_ONE_PLANE, [plane, ], three_circle)
        #         if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
        #             max_circle_area = area
        #             max_circle = area.inner_circle()
        #
        # # 两个面，两个圆
        # for two_plane in itertools.combinations(planes, 2):
        #     if not two_plane[0].parallel_to(two_plane[1]):
        #         two_circles = itertools.combinations(circles, 2)
        #         for two_circle in two_circles:
        #             area = Area(Area.Type.TWO_CIRCLE_TWO_PLANE, two_plane, two_circle)
        #             if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
        #                 max_circle_area = area
        #                 max_circle = area.inner_circle()
        #
        # # 三个面，一个圆
        # for three_plane in itertools.combinations(planes, 3):
        #     if not three_plane[0].parallel_to(three_plane[1]) and \
        #             not three_plane[1].parallel_to(three_plane[2]) and \
        #             not three_plane[2].parallel_to(three_plane[0]):
        #         for circle in circles:
        #             area = Area(Area.Type.ONE_CIRCLE_THREE_PLANE, three_plane, [circle, ])
        #             if area.inner_circle().r > max_circle.r and check_area(area, circles, planes):
        #                 max_circle_area = area
        #                 max_circle = area.inner_circle()


        if max_circle_area is not None:
            # 找到了当前最大的圆
            # 移除圆周上的障碍，这些点已经不能看作半径为 0 的圆了
            for c in max_circle_area.circles:
                if c.r == 0:
                    circles.remove(c)
            circles.append(max_circle)
            m -= 1

    # 移除所有障碍
    for c in circles:
        if c.r == 0:
            circles.remove(c)
    return circles


bk1 = Circle(0, 0, 0, 0)
bk2 = Circle(0.5, 0.5, 0.5, 0)
bk3 = Circle(-0.6, -0.5, -0.5, 0)
bk4 = Circle(-0.5, 0.5, 0.5, 0)
bk5 = Circle(0.3, -0.7, -0.5, 0)
bks1 = [bk1]
bks2 = [bk1, bk2]
bks3 = [bk1, bk2, bk3]
bks4 = [bk1, bk2, bk3, bk4]
bks5 = [bk1, bk2, bk3, bk4, bk5]
blocks = [bks1, bks2, bks3, bks4, bks5]

# for bks in blocks:
#     result = main(30, bks)
#     plot(result, bks, "result" + str(len(bks)))

result = main(10, bks5)
for circle in result:
    print (circle.x, circle.y, circle.z, circle.r)

plot(result, bks3, None)
