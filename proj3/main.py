#!/usr/bin/env python2

from compute import *
from drawer import *

bk1 = Sphere(0, 0, 0, 0)
bk2 = Sphere(0.5, 0.5, 0.5, 0)
bk3 = Sphere(-0.6, -0.5, -0.5, 0)
bk4 = Sphere(-0.5, 0.5, 0.5, 0)
bk5 = Sphere(0.3, -0.7, -0.5, 0)
bks1 = [bk1]
bks2 = [bk1, bk2]
bks3 = [bk1, bk2, bk3]
bks4 = [bk1, bk2, bk3, bk4]
bks5 = [bk1, bk2, bk3, bk4, bk5]
blocks = [bks1, bks2, bks3, bks4, bks5]

result = compute(10, bks5)
# for circle in result:
#     print circle.x, circle.y, circle.z, circle.r

plot(result, bks3, None)