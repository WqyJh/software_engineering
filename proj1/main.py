#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scipy.optimize import fsolve
import numpy as np
import math
import turtle


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r


class Edge(object):
    def __init__(self, point1, point2):
        self.A = point2.y - point1.y
        self.B = point1.x - point2.x
        self.C = point2.x * point1.y - point1.x * point2.y


# edge1 represents a edge that's perpendicular to the X axis
# edge2 represents a edge that's parallel to the X axis
def one_circle_two_edge(circle1, edge1, edge2):
    if edge1.A == 0:
        edge1, edge2 = edge2, edge1
    r = (math.sqrt(2) - 1) / (math.sqrt(2) + 1) * circle1.r
    x2 = -edge1.C / edge1.A
    y3 = -edge2.C / edge2.B
    x = x2 - r if x2 > circle1.x else x2 + r
    y = y3 - r if y3 > circle1.y else y3 + r
    return Circle(x, y, r)


# def two_circle_one_edge(circle1, circle2, edge):
#     r1, r2 = circle1.r, circle2.r
#     r = pow(math.sqrt(r1 * r2) / (math.sqrt(r1) + math.sqrt(r2)), 2)
#
#     def equations(p):
#         x, y = p
#         return (pow(x - circle1.x, 2) + pow(y - circle1.y, 2) - pow(r + circle1.r, 2),
#                 pow(x - circle2.x, 2) + pow(y - circle2.y, 2) - pow(r + circle2.r, 2),)
#                 # abs(edge.A * x + edge.B * y + edge.C) - r * math.sqrt(edge.A * edge.A + edge.B * edge.B))
#
#     x, y = fsolve(equations, (0, 0, 0))
#     return Circle(x, y, r)

def two_circle_one_edge(circle1, circle2, edge):
    r1, r2 = circle1.r, circle2.r
    x1, x2 = circle1.x, circle2.x
    y1, y2 = circle1.y, circle2.y
    r = pow(math.sqrt(r1 * r2) / (math.sqrt(r1) + math.sqrt(r2)), 2)
    x = y = 0
    if edge.A == 0:
        y3 = -edge.C / edge.B
        y = y3 + r if y3 < circle1.y else y3 - r
        x = (-2 * (y1 - y2) * y + 2 * (r2 - r1) * r + r2 * r2 - r1 * r1 + x1 * x1 - x2 * x2 + y1 * y1 - y2 * y2) / (
            2 * (x1 - x2))
    if edge.B == 0:
        x3 = -edge.C / edge.A
        x = x3 + r if x3 < circle1.x else x3 - r
        y = (-2 * (x1 - x2) * x + 2 * (r2 - r1) * r + r2 * r2 - r1 * r1 + x1 * x1 - x2 * x2 + y1 * y1 - y2 * y2) / (
            2 * (y1 - y2))
    return Circle(x, y, r)


def three_circle(circle1, circle2, circle3):
    x1, y1, r1 = circle1.x, circle1.y, circle1.r
    x2, y2, r2 = circle2.x, circle2.y, circle2.r
    x3, y3, r3 = circle3.x, circle3.y, circle3.r

    a = np.array([
        [x1 - x2, y1 - y2, r1 - r2],
        [x2 - x3, y2 - y3, r2 - r3],
        [x1 - x3, y1 - y3, r1 - r3]
    ])
    b = np.array([
        1 / 2 * (r2 * r2 - r1 * r1 + y1 * y1 - y2 * y2 + x1 * x1 - x2 * x2),
        1 / 2 * (r3 * r3 - r2 * r2 + y2 * y2 - y3 * y3 + x2 * x2 - x3 * x3),
        1 / 2 * (r2 * r1 - r1 * r1 + y1 * y1 - y3 * y3 + x1 * x1 - x3 * x3),
    ])
    x, y, r = np.linalg.solve(a, b)
    return Circle(x, y, r)


class Area(object):
    def __init__(self, type, edges, circles):
        self.type = type
        self.edges = edges
        self.circles = circles
        self.circle = None

    class Type(object):
        ONE_CIRCLE_TWO_EDGE = 0
        TWO_CIRCLE_ONE_EDGE = 1
        THREE_CIRCLE = 3

    def inner_circle(self):
        if self.circle == None:
            if self.type == Area.Type.ONE_CIRCLE_TWO_EDGE:
                self.circle = one_circle_two_edge(self.circles[0], self.edges[0], self.edges[1])
            elif self.type == Area.Type.TWO_CIRCLE_ONE_EDGE:
                self.circle = two_circle_one_edge(self.circles[0], self.circles[1], self.edges[0])
            elif self.type == Area.Type.THREE_CIRCLE:
                self.circle = three_circle(self.circles[0], self.circles[1], self.circles[2])
        return self.circle

    def new_areas(self, inner_circle):
        if self.type == Area.Type.ONE_CIRCLE_TWO_EDGE:
            return [Area(Area.Type.ONE_CIRCLE_TWO_EDGE, self.edges, [inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[0]], [self.circles[0], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[1]], [self.circles[0], inner_circle])]

        elif self.type == Area.Type.TWO_CIRCLE_ONE_EDGE:
            return [Area(Area.Type.THREE_CIRCLE, None, [self.circles[0], self.circles[1], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[0]], [self.circles[0], inner_circle]),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, [self.edges[0]], [self.circles[1], inner_circle])]
        elif self.type == Area.Type.THREE_CIRCLE:
            return [Area(Area.Type.THREE_CIRCLE, None, [self.circles[0], self.circles[1], inner_circle]),
                    Area(Area.Type.THREE_CIRCLE, None, [self.circles[0], self.circles[2], inner_circle]),
                    Area(Area.Type.THREE_CIRCLE, None, [self.circles[1], self.circles[2], inner_circle])]


def plot(result):
    turtle.penup()
    turtle.goto(-300, 300)  # 左上角
    turtle.pendown()
    turtle.forward(600)  # 右上角
    turtle.right(90)  # 向下
    turtle.forward(600)  # 右下角
    turtle.right(90)  # 向左
    turtle.forward(600)  # 左下角
    turtle.right(90)  # 向上
    turtle.forward(600)  # 左上角
    for circle in result:
        turtle.penup()
        turtle.goto((circle.x + circle.r) * 300, circle.y)
        turtle.pendown()
        turtle.circle(circle.r * 300)
    turtle.exitonclick()


def main(m):
    queue = []
    result = []
    circle0 = Circle(0, 0, 1)
    edge1 = Edge(Point(1, 1), Point(1, -1))
    edge2 = Edge(Point(1, 1), Point(-1, 1))
    edge3 = Edge(Point(-1, 1), Point(-1, -1))
    edge4 = Edge(Point(-1, -1), Point(1, -1))
    result.append(circle0)
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, [edge1, edge2], [circle0]))
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, [edge2, edge3], [circle0]))
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, [edge3, edge4], [circle0]))
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, [edge4, edge1], [circle0]))
    while len(queue) > 0 and m >= 0:
        area = queue.pop()
        circle = area.inner_circle()
        for i in range(0, len(queue)):  # 选出圆面积最大的区域
            if queue[i].inner_circle().r > circle.r:
                queue.append(area)
                area = queue.pop(i)
                circle = area.inner_circle()  # 总是取最大的这个圆
        areas = area.new_areas(circle)
        queue = queue + areas  # 将新产生的区域加到队列中
        result.append(circle)
        m -= 1
    return result


result = main(100)
plot(result)
