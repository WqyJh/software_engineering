#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
from scipy.optimize import fsolve
from math import sqrt
import itertools
import multiprocessing

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


class Sphere(object):
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def intersect_with(self, sphere):
        d1 = pow(self.x - sphere.x, 2) + pow(self.y - sphere.y, 2) + pow(self.z - sphere.z, 2)
        d2 = pow(self.r + sphere.r, 2)
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


def one_sphere_three_plane(sphere1, plane1, plane2, plane3):
    x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
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

    ((x, y, z, r), info, status, mesg) = fsolve(equations, (x0, y0, z0, r0), full_output=True)
    if status == 1:
        return Sphere(x, y, z, r)
    else:
        return Sphere(0, 0, 0, 0)


def two_sphere_two_plane(sphere1, sphere2, plane1, plane2):
    x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
    x2, y2, z2, r2 = sphere2.x, sphere2.y, sphere2.z, sphere2.r

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

    ((x, y, z, r), info, status, mesg) = fsolve(equations, (x0, y0, z0, r0), full_output=True)
    if status == 1:
        return Sphere(x, y, z, r)
    else:
        return Sphere(0, 0, 0, 0)


def three_sphere_one_plane(sphere1, sphere2, sphere3, plane):
    x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
    x2, y2, z2, r2 = sphere2.x, sphere2.y, sphere2.z, sphere2.r
    x3, y3, z3, r3 = sphere3.x, sphere3.y, sphere3.z, sphere3.r

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

    ((x, y, z, r), info, status, mesg) = fsolve(equations, (x0, y0, z0, r0), full_output=True)
    if status == 1:
        return Sphere(x, y, z, r)
    else:
        # print(mesg)
        return Sphere(0, 0, 0, 0)


def four_sphere(sphere1, sphere2, sphere3, sphere4):
    sphere1, sphere2, sphere3, sphere4 = sorted([sphere1, sphere2, sphere3, sphere4])

    x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
    x2, y2, z2, r2 = sphere2.x, sphere2.y, sphere2.z, sphere2.r
    x3, y3, z3, r3 = sphere3.x, sphere3.y, sphere3.z, sphere3.r
    x4, y4, z4, r4 = sphere4.x, sphere4.y, sphere4.z, sphere4.r

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

    ((x, y, z, r), info, status, mesg) = fsolve(equations, (x0, y0, z0, r0), full_output=True)
    if status == 1:
        return Sphere(x, y, z, r)
    else:
        return Sphere(0, 0, 0, 0)


def sphere_filter(spheres):
    """
    过滤出半径大于0的球
    :param spheres:
    :return:
    """
    list = []
    for sphere in spheres:
        if sphere.r > 0:
            list.append(sphere)
    return list


class Area(object):
    def __init__(self, atype, planes, spheres):
        self.atype = atype
        self.planes = planes
        self.spheres = spheres
        self.in_sphere = None

    class Type(object):
        ONE_SPHERE_THREE_PLANE = 0
        TWO_SPHERE_TWO_PLANE = 1
        THREE_SPHERE_ONE_PLANE = 2
        FOUR_SPHERE = 3

    def inner_sphere(self):
        if self.in_sphere is None:
            if self.atype == Area.Type.ONE_SPHERE_THREE_PLANE:
                self.in_sphere = one_sphere_three_plane(self.spheres[0], self.planes[0], self.planes[1], self.planes[2])
            elif self.atype == Area.Type.TWO_SPHERE_TWO_PLANE:
                self.in_sphere = two_sphere_two_plane(self.spheres[0], self.spheres[1], self.planes[0], self.planes[1])
            elif self.atype == Area.Type.THREE_SPHERE_ONE_PLANE:
                self.in_sphere = three_sphere_one_plane(self.spheres[0], self.spheres[1], self.spheres[2],
                                                        self.planes[0])
            elif self.atype == Area.Type.FOUR_SPHERE:
                self.in_sphere = four_sphere(self.spheres[0], self.spheres[1], self.spheres[2], self.spheres[3])
        return self.in_sphere

    def new_areas(self, inner_sphere):
        if self.atype == Area.Type.ONE_SPHERE_THREE_PLANE:
            return [Area(Area.Type.ONE_SPHERE_THREE_PLANE, self.planes, [inner_sphere, ]),
                    Area(Area.Type.TWO_SPHERE_TWO_PLANE, [self.planes[0], self.planes[1]],
                         [self.spheres[0], inner_sphere]),
                    Area(Area.Type.TWO_SPHERE_TWO_PLANE, [self.planes[0], self.planes[2]],
                         [self.spheres[0], inner_sphere]),
                    Area(Area.Type.TWO_SPHERE_TWO_PLANE, [self.planes[1], self.planes[2]],
                         [self.spheres[0], inner_sphere])]
        elif self.atype == Area.Type.TWO_SPHERE_TWO_PLANE:
            return [Area(Area.Type.TWO_SPHERE_TWO_PLANE, self.planes, [self.spheres[0], inner_sphere]),
                    Area(Area.Type.TWO_SPHERE_TWO_PLANE, self.planes, [self.spheres[1], inner_sphere]),
                    Area(Area.Type.THREE_SPHERE_ONE_PLANE, self.planes[0],
                         [self.spheres[0], self.spheres[1], inner_sphere]),
                    Area(Area.Type.THREE_SPHERE_ONE_PLANE, self.planes[1],
                         [self.spheres[0], self.spheres[1], inner_sphere])]
        elif self.atype == Area.Type.FOUR_SPHERE:
            return [Area(Area.Type.FOUR_SPHERE, [], [self.spheres[0], self.spheres[1], self.spheres[2], inner_sphere]),
                    Area(Area.Type.FOUR_SPHERE, [], [self.spheres[0], self.spheres[1], self.spheres[3], inner_sphere]),
                    Area(Area.Type.FOUR_SPHERE, [], [self.spheres[0], self.spheres[2], self.spheres[3], inner_sphere]),
                    Area(Area.Type.FOUR_SPHERE, [], [self.spheres[1], self.spheres[2], self.spheres[3], inner_sphere])]


# 检查 area 是否合法
def check_area(area, spheres, planes):
    sphere = area.inner_sphere()
    for c in spheres:
        if sphere.intersect_with(c):
            return False
    for plane in planes:
        if float_lt(plane.dist_to_point(sphere.x, sphere.y, sphere.z), sphere.r):
            return False
    return True


def sphere_exists(spheres, sphere):
    for c in spheres:
        if c.equals(sphere):
            return True
    return False


def sumr2(result):
    s = 0
    for sphere in result:
        s += sphere.r * sphere.r
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


def compute_four_sphere(spheres, planes):
    max_sphere_area = None
    max_sphere = Sphere(0, 0, 0, 0)
    for four_sphere in itertools.combinations(spheres, 4):
        area = Area(Area.Type.FOUR_SPHERE, [], four_sphere)
        if area.inner_sphere().r > max_sphere.r and check_area(area, spheres, planes):
            max_sphere_area = area
            max_sphere = area.inner_sphere()
    return (max_sphere_area, max_sphere)


def compute_three_sphere_one_plane(spheres, planes):
    max_sphere_area = None
    max_sphere = Sphere(0, 0, 0, 0)
    for plane in planes:
        three_spheres = itertools.combinations(spheres, 3)
        for three_sphere in three_spheres:
            area = Area(Area.Type.THREE_SPHERE_ONE_PLANE, [plane, ], three_sphere)
            if area.inner_sphere().r > max_sphere.r and check_area(area, spheres, planes):
                max_sphere_area = area
                max_sphere = area.inner_sphere()
    return (max_sphere_area, max_sphere)


def compute_two_sphere_two_plane(spheres, planes):
    max_sphere_area = None
    max_sphere = Sphere(0, 0, 0, 0)
    for two_plane in itertools.combinations(planes, 2):
        if not two_plane[0].parallel_to(two_plane[1]):
            two_spheres = itertools.combinations(spheres, 2)
            for two_sphere in two_spheres:
                area = Area(Area.Type.TWO_SPHERE_TWO_PLANE, two_plane, two_sphere)
                if area.inner_sphere().r > max_sphere.r and check_area(area, spheres, planes):
                    max_sphere_area = area
                    max_sphere = area.inner_sphere()
    return (max_sphere_area, max_sphere)


def compute_one_sphere_three_plane(spheres, planes):
    max_sphere_area = None
    max_sphere = Sphere(0, 0, 0, 0)
    for three_plane in itertools.combinations(planes, 3):
        if not three_plane[0].parallel_to(three_plane[1]) and \
                not three_plane[1].parallel_to(three_plane[2]) and \
                not three_plane[2].parallel_to(three_plane[0]):
            for sphere in spheres:
                area = Area(Area.Type.ONE_SPHERE_THREE_PLANE, three_plane, [sphere, ])
                if area.inner_sphere().r > max_sphere.r and check_area(area, spheres, planes):
                    max_sphere_area = area
                    max_sphere = area.inner_sphere()
    return (max_sphere_area, max_sphere)


def compute(m, blocks):
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

    spheres = [] + blocks
    output = []

    pool = multiprocessing.Pool(4)

    while m > 0:
        max_sphere_area = None
        max_sphere = Sphere(0, 0, 0, 0)

        output.clear()

        output.append(pool.apply_async(compute_four_sphere, (spheres, planes)))
        output.append(pool.apply_async(compute_three_sphere_one_plane, (spheres, planes)))
        output.append(pool.apply_async(compute_two_sphere_two_plane, (spheres, planes)))
        output.append(pool.apply_async(compute_one_sphere_three_plane, (spheres, planes)))

        for opt in output:
            (m_c_a, m_c) = opt.get()
            if m_c.r > max_sphere.r:
                max_sphere_area = m_c_a
                max_sphere = m_c

        if max_sphere_area is not None:
            # 找到了当前最大的球
            # 移除球面上的障碍，这些点已经不能看作半径为 0 的球了
            for c in max_sphere_area.spheres:
                if c.r == 0:
                    spheres.remove(c)
            spheres.append(max_sphere)
            m -= 1

    # 移除所有障碍
    for c in spheres:
        if c.r == 0:
            spheres.remove(c)
    return spheres
