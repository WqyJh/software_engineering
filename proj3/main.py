#!/usr/bin/env python

from compute import *
from drawer import *

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

result = main(15, bks5)
# for circle in result:
#     print circle.x, circle.y, circle.z, circle.r

plot(result, bks3, None)