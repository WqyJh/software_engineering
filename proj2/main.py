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


def float_equals(f1, f2):
    return abs(f1 - f2) < EPSINON


def float_lt(f1, f2):
    if not float_equals(f1, f2):
        return f1 < f2
    return False


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
        if not float_equals(d1, d2):
            return d1 < d2
        return False

    def __eq__(self, other):
        return float_equals(self.x, other.x) and float_equals(self.y, other.y) and float_equals(self.r, other.r)


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
        # y0 = (y0 - x3) / 2  # y0移动后，相当于(x0,y0)沿两圆心的中垂线移动
    else:
        y3 = -edge.C / edge.B
        y0 = (y0 + y3) / 2  # y0向y3方向移动
        # x0 = (x0 - y3) / 2  # x0移动后，相当于(x0,y0)沿两圆心的中垂线移动

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
            if self.circles[0].r == 0:
                return [Area(Area.Type.ONE_CIRCLE_TWO_EDGE, self.edges, [inner_circle, ])]
            return [Area(Area.Type.ONE_CIRCLE_TWO_EDGE, self.edges, [inner_circle, ]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[0], ], [self.circles[0], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[1], ], [self.circles[0], inner_circle])]
        elif self.atype == Area.Type.TWO_CIRCLE_ONE_EDGE:
            if self.circles[0].r == 0 and self.circles[1].r == 0:
                return []
            elif self.circles[0].r == 0 or self.circles[1].r == 0:
                c = self.circles[0] if self.circles[0].r != 0 else self.circles[1]
                return [Area(Area.Type.TWO_CIRCLE_ONE_EDGE, self.edges, [inner_circle, c])]
            return [Area(Area.Type.THREE_CIRCLE, [], [self.circles[0], self.circles[1], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[0], ], [self.circles[0], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[0], ], [self.circles[1], inner_circle])]
        elif self.atype == Area.Type.THREE_CIRCLE:
            filtered_circle = circle_filter(self.circles)
            if len(filtered_circle) == 0 or len(filtered_circle) == 1:
                return []
            elif len(filtered_circle) == 2:
                return [Area(Area.Type.THREE_CIRCLE, [], [filtered_circle[0], filtered_circle[1], inner_circle])]
            return [Area(Area.Type.THREE_CIRCLE, [], [self.circles[0], self.circles[1], inner_circle]),
                    Area(Area.Type.THREE_CIRCLE, [], [self.circles[0], self.circles[2], inner_circle]),
                    Area(Area.Type.THREE_CIRCLE, [], [self.circles[1], self.circles[2], inner_circle])]


# 检查 area 是否合法
def check_area(area, circles, edges):
    circle = area.inner_circle()
    for c in circles:
        if circle.intersect_with(c):
            return False
    for edge in edges:
        if float_lt(edge.dist_to_point(circle.x, circle.y), circle.r):
            return False
    return True


def circle_exists(circles, circle):
    for c in circles:
        if c == circle:
            return True
    return False


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
    """
    离边最近的两个圆
    :param edge:
    :param circles:
    :return: (circle1, circle2) 其中 circle1 为最邻近
    """
    if len(circles) < 2:
        return []
    circle1 = circles[0]
    circle2 = circles[1]
    d1 = edge.dist_to_point(circle1.x, circle1.y) - circle1.r
    d2 = edge.dist_to_point(circle2.x, circle2.y) - circle2.r
    if float_lt(d2, d1):
        circle1, circle2 = circle2, circle1

    for i in range(2, len(circles)):
        c = circles[i]
        d = edge.dist_to_point(c.x, c.y) - c.r
        if d < edge.dist_to_point(circle1.x, circle1.y) - circle1.r:
            circle1 = c
        elif d < edge.dist_to_point(circle2.x, circle2.y) - circle2.r:
            circle2 = c
    return [circle1, circle2]


def find_two_circle(edge, circles):
    """
    找到可以与边构成区域的两个圆的集合
    :param edge:
    :param circles:
    :return:
    """
    two_circles = []
    edges = [edge, ]
    for two_circle in itertools.combinations(circles, 2):
        area = Area(Area.Type.TWO_CIRCLE_ONE_EDGE, edges, two_circle)
        if check_area(area, circles, edges):
            two_circles.append(two_circle)
    return two_circles


def nearest_one_circle(edge1, edge2, circles):
    circle = circles[0]
    edges = [edge1, edge2]
    min_area = Area(Area.Type.ONE_CIRCLE_TWO_EDGE, edges, [circle, ])

    for i in range(1, len(circles)):
        area = Area(Area.Type.ONE_CIRCLE_TWO_EDGE, edges, [circles[i], ])
        if min_area.inner_circle().r > area.inner_circle().r:
            min_area = area
            circle = circles[i]
    return circle


def plot(result, blocks, name):
    scale = 400
    turtle.hideturtle()
    turtle.tracer(False)
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

    block_radius = 4
    for block in blocks:
        turtle.penup()
        turtle.goto(block.x * scale + block_radius, block.y * scale)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(block_radius)
        turtle.end_fill()

    for circle in result:
        turtle.penup()
        turtle.goto((circle.x + circle.r) * scale, circle.y * scale)
        turtle.pendown()
        turtle.circle(circle.r * scale)
        ts = turtle.getscreen().getcanvas()
        canvasvg.saveall(name + ".svg", ts)
    turtle.hideturtle()
    # turtle.exitonclick()


def sumr2(result):
    s = 0
    for circle in result:
        s += circle.r * circle.r
    return s


def block_filter(blocks, edges):
    """
    过滤掉无效的障碍。在边界上的障碍为无效障碍
    :param blocks:
    :return:
    """
    for block in blocks:
        for edge in edges:
            if float_equals(0, edge.dist_to_point(block.x, block.y)):
                blocks.remove(block)
    return blocks


def main(m, blocks):
    edge1 = Edge(Point(1, 1), Point(1, -1))
    edge2 = Edge(Point(1, -1), Point(-1, -1))
    edge3 = Edge(Point(-1, -1), Point(-1, 1))
    edge4 = Edge(Point(-1, 1), Point(1, 1))
    edges = [edge1, edge2, edge3, edge4]
    block_filter(blocks, edges)

    circles = [] + blocks
    # queue = []
    # for two_edge in sequence_combination(edges, 2):
    #     c = nearest_one_circle(two_edge[0], two_edge[1], blocks)
    #     queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, two_edge, [c, ]))
    # for edge in edges:
    #     two_circle = nearest_two_circle(edge, blocks)
    #     if len(two_circle) > 0:
    #         queue.append(Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [edge, ], two_circle))
    # for three_c in itertools.combinations(blocks, 3):
    #     queue.append(Area(Area.Type.THREE_CIRCLE, [], three_c))
    #
    # while len(queue) > 0 and m > 0:
    #     area = queue.pop()
    #     inner_circle = area.inner_circle()
    #
    #     # print inner_circle.r
    #     for i in range(len(queue)):
    #         # print queue[i].inner_circle().r
    #         if float_lt(inner_circle.r, queue[i].inner_circle().r):
    #         # if queue[i].inner_circle().r > inner_circle.r:
    #             queue.insert(i + 1, area)
    #             area = queue.pop(i)
    #             inner_circle = area.inner_circle()
    #
    #     if not check_area(area, circles, edges):
    #         continue
    #
    #     areas = area.new_areas(inner_circle)
    #     queue = queue + areas  # 将新产生的区域加到队列中
    #
    #     # 找出区域中对应的障碍
    #     for c in area.circles:
    #         if c.r == 0:
    #             # 遍历所有区域，把该障碍替换成这个圆
    #             for i in range(len(queue)):
    #                 cls = queue[i].circles
    #                 for j in range(len(cls)):
    #                     if cls[j] == c:
    #                         cls.pop(j)
    #                         cls.insert(j, inner_circle)
    #                         queue[i].in_circle = None
    #
    #     if not circle_exists(circles, inner_circle):
    #         circles.append(inner_circle)
    #         m -= 1
    # return circles

    while m > 0:
        max_circle_area = None
        max_circle = Circle(0, 0, 0)
        # 一条边，两个圆
        for edge in edges:
            # two_circles = find_two_circle(edge, circles)
            two_circles = itertools.combinations(circles, 2)
            for two_circle in two_circles:
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
                    circles.remove(c)
            circles.append(max_circle)
            m -= 1

    # 移除所有障碍
    for c in circles:
        if c.r == 0:
            circles.remove(c)
    return circles


bk1 = Circle(0, 0, 0)
bk2 = Circle(0.5, 0.5, 0)
bk3 = Circle(-0.6, -0.5, 0)
bk4 = Circle(-0.5, 0.5, 0)
bk5 = Circle(0.3, -0.7, 0)
bks1 = [bk1]
bks2 = [bk1, bk2]
bks3 = [bk1, bk2, bk3]
bks4 = [bk1, bk2, bk3, bk4]
bks5 = [bk1, bk2, bk3, bk4, bk5]
blocks = [bks1, bks2, bks3, bks4, bks5]

for bks in blocks:
    result = main(30, bks)
    plot(result, bks, "result" + str(len(bks)))
