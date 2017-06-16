#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scipy.optimize import fsolve
import numpy as np
from math import sqrt
import turtle
import canvasvg
import itertools
import pylab

EPSINON = 1e-6


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def intersect_with(self, circle):
        d1 = pow(self.x - circle.x, 2) + pow(self.y - circle.y, 2)
        d2 = pow(self.r + circle.r, 2)
        if (abs(d1 - d2) > EPSINON):
            return d1 < d2
        return False


class Edge(object):
    def __init__(self, point1, point2):
        self.A = point2.y - point1.y
        self.B = point1.x - point2.x
        self.C = point2.x * point1.y - point1.x * point2.y

    def dist_to_point(self, x, y):
        return abs(self.A * x + self.B * y + self.C) / sqrt(self.A * self.A + self.B * self.B)


# edge1 represents a edge that's perpendicular to the X axis
# edge2 represents a edge that's parallel to the X axis
def one_circle_two_edge(circle1, edge1, edge2):
    x1, y1, r1 = circle1.x, circle1.y, circle1.r
    if edge1.A == 0:
        edge1, edge2 = edge2, edge1

    x2 = -edge1.C / edge1.A
    y3 = -edge2.C / edge2.B
    x0 = (x1 + x2) / 2
    y0 = (y1 + y3) / 2
    r0 = min(edge1.dist_to_point(x0, y0), edge2.dist_to_point(x0, y0))

    def equations(p):
        x, y, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) - pow(r + r1, 2),
                edge1.dist_to_point(x, y) - r,
                edge2.dist_to_point(x, y) - r)

    ((x, y, r), info, status, mesg) = fsolve(equations, (x0, y0, r0), full_output=True)

    if status == 1:
        return Circle(x, y, r)
    else:
        # print mesg
        # print x0, y0, r0
        # print x, y, r
        return Circle(0, 0, 0)


def two_circle_one_edge(circle1, circle2, edge):
    x1, y1, r1 = circle1.x, circle1.y, circle1.r
    x2, y2, r2 = circle2.x, circle2.y, circle2.r

    # 估算圆心的值
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2

    if edge.B == 0:
        x3 = -edge.C / edge.A
        x0 = (x0 + x3) / 2  # x0向x3方向移动
        y0 = (y0 - x3) / 2  # y0移动后，相当于(x0,y0)沿两圆心的中垂线移动
    else:
        y3 = -edge.C / edge.B
        y0 = (y0 + y3) / 2  # y0向y3方向移动
        x0 = (x0 - y3) / 2  # x0移动后，相当于(x0,y0)沿两圆心的中垂线移动

    r0 = edge.dist_to_point(x0, y0)

    def equations(p):
        x, y, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) - pow(r + r1, 2),
                pow(x - x2, 2) + pow(y - y2, 2) - pow(r + r2, 2),
                edge.dist_to_point(x, y) - r)

    ((x, y, r), info, status, mesg) = fsolve(equations, (x0, y0, r0), full_output=True)

    if status == 1:
        return Circle(x, y, r)
    else:
        # if x0 > 0 and y0 > 0:
        #     print mesg
        #     print x0, y0, r0
        #     print x, y, r
        return Circle(0, 0, 0)


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


class Area(object):
    def __init__(self, atype, edges, circles):
        self.atype = atype
        self.edges = edges
        self.circles = circles
        self.in_circle = None

    class Type(object):
        ONE_CIRCLE_TWO_EDGE = 0
        TWO_CIRCLE_ONE_EDGE = 1
        THREE_CIRCLE = 2

    def inner_circle(self):
        if self.in_circle is None:
            if self.atype == Area.Type.ONE_CIRCLE_TWO_EDGE:
                self.in_circle = one_circle_two_edge(self.circles[0], self.edges[0], self.edges[1])
            elif self.atype == Area.Type.TWO_CIRCLE_ONE_EDGE:
                self.in_circle = two_circle_one_edge(self.circles[0], self.circles[1], self.edges[0])
            elif self.atype == Area.Type.THREE_CIRCLE:
                self.in_circle = three_circle(self.circles[0], self.circles[1], self.circles[2])
        return self.in_circle

    def new_areas(self, inner_circle):
        if self.atype == Area.Type.ONE_CIRCLE_TWO_EDGE:
            return [Area(Area.Type.ONE_CIRCLE_TWO_EDGE, self.edges, (inner_circle,)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[0],), (self.circles[0], inner_circle)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[1],), (self.circles[0], inner_circle))]
        elif self.atype == Area.Type.TWO_CIRCLE_ONE_EDGE:
            return [Area(Area.Type.THREE_CIRCLE, (), (self.circles[0], self.circles[1], inner_circle)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[0],), (self.circles[0], inner_circle)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[0],), (self.circles[1], inner_circle))]
        elif self.atype == Area.Type.THREE_CIRCLE:
            return [Area(Area.Type.THREE_CIRCLE, (), (self.circles[0], self.circles[1], inner_circle)),
                    Area(Area.Type.THREE_CIRCLE, (), (self.circles[0], self.circles[2], inner_circle)),
                    Area(Area.Type.THREE_CIRCLE, (), (self.circles[1], self.circles[2], inner_circle))]


# 检查 area 是否合法
def check_area(area, circles, edges):
    circle = area.inner_circle()
    for c in circles:
        if circle.intersect_with(c):
            return False
    for edge in edges:
        if circle.r > edge.dist_to_point(circle.x, circle.y):
            return False
    return True


def sequence_combination(list, n):
    l = []
    length = len(list)
    for i in range(length):
        if i + n <= length:
            l.append(list[i:i + n])
        else:
            l.append(list[i:] + list[0:n - length + i])
    return l


def nearest_two_circle(edge, circles):
    circle1 = Circle(0, 0, 2)
    circle2 = Circle(0, 0, 2)

    for c in circles:
        d = edge.dist_to_point(c.x, c.y) - c.r
        if d < edge.dist_to_point(circle1.x, circle1.y):
            circle1 = c
        elif d < edge.dist_to_point(circle2.x, circle2.y):
            circle2 = c
    return (circle1, circle2)


def nearest_one_circle(edge1, edge2, circles):
    circle = None
    dist = 4.0
    if edge1.A == 0:
        edge1, edge2 = edge2, edge1
    x = -edge1.C / edge1.A
    y = -edge2.C / edge2.B
    for c in circles:
        d = sqrt(pow(x - c.x, 2) + pow(y - c.y, 2)) - c.r
        if dist > d:
            dist = d
            circle = c
    return circle


def plot(result, name):
    scale = 400
    # turtle.tracer(False)
    turtle.speed("fast")
    turtle.clear()
    turtle.penup()
    turtle.home()
    turtle.goto(-scale, scale)  # 左上角
    turtle.pendown()
    turtle.forward(scale * 2)  # 右上角
    turtle.right(90)  # 向下
    turtle.forward(scale * 2)  # 右下角
    turtle.right(90)  # 向左
    turtle.forward(scale * 2)  # 左下角
    turtle.right(90)  # 向上
    turtle.forward(scale * 2)  # 左上角
    # print "len = ", len(result)
    for circle in result:
        # print circle.x, circle.y, circle.r
        turtle.penup()
        turtle.goto((circle.x + circle.r) * scale, circle.y * scale)
        turtle.pendown()
        turtle.circle(circle.r * scale)
        # ts = turtle.getscreen().getcanvas()
        # canvasvg.saveall(name + ".svg", ts)


def sumr2(result):
    s = 0
    for circle in result:
        s += circle.r * circle.r
    # print "sum r^2 = ", s
    return s


def main(m, blocks):
    edge1 = Edge(Point(1, 1), Point(1, -1))
    edge2 = Edge(Point(1, -1), Point(-1, -1))
    edge3 = Edge(Point(-1, -1), Point(-1, 1))
    edge4 = Edge(Point(-1, 1), Point(1, 1))

    edges = [edge1, edge2, edge3, edge4]
    circles = list(blocks)
    quque = []

    while m > 0:
        max_circle_area = None
        max_circle = Circle(0, 0, 0)
        # 一条边，两个圆
        for edge in edges:
            two_circle = nearest_two_circle(edge, circles)
            area = Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (edge,), two_circle)
            if area.inner_circle().r > max_circle.r and check_area(area, circles, edges):
                # if area.inner_circle().r > max_circle.r:
                max_circle_area = area
                max_circle = area.inner_circle()

        # 两条边，一个圆
        for two_edge in sequence_combination(edges, 2):
            c = nearest_one_circle(two_edge[0], two_edge[1], circles)
            area = Area(Area.Type.ONE_CIRCLE_TWO_EDGE, two_edge, (c,))
            if area.inner_circle().r > max_circle.r and check_area(area, circles, edges):
                # if area.inner_circle().r > max_circle.r:
                max_circle_area = area
                max_circle = area.inner_circle()

        # 三个圆
        for three_circle in itertools.combinations(circles, 3):
            area = Area(Area.Type.THREE_CIRCLE, (), three_circle)
            if area.inner_circle().r > max_circle.r and check_area(area, circles, edges):
                # if area.inner_circle().r > max_circle.r:
                max_circle_area = area
                max_circle = area.inner_circle()

        if max_circle_area is not None:
            # 找到了当前最大的圆
            # 移除圆周上的障碍，这些点已经不能看作半径为 0 的圆了
            for c in max_circle_area.circles:
                if c.r == 0:
                    print "x, y, r = ", c.x, c.y, c.r
                    circles.remove(c)
            circles.append(max_circle)
            # for circle in circles:
            # print "circle: x, y, r", circle.x, circle.y, circle.r
            # print "\n"
            m -= 1

    # 移除所有障碍
    # for c in circles:
    #     if c.r == 0:
    #         circles.remove(c)

    return circles


ms = [10, 20, 30, 50, 80, 100, 200, 300, 400, 500]
blocks = []
blocks.append(Circle(0, 0, 0))
result = main(20, blocks)
print "length of result = ", len(result)
plot(result, "test")
# sums = []
# for m in ms:
#     result = main(m)
#     plot(result, "result" + str(m))
#     sums.append(sumr2(result))
#
# pylab.plot(ms, sums)
# pylab.savefig("sum.png")
