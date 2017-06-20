#!/usr/bin/env python3
from compute import *
import user_interface as ui

# from drawer import plot


p = ui.start()
if p == None or len(p) < 2:
    exit(0)

(m, data) = p

blocks = []
for (x, y, z, r) in data:
    blocks.append(Sphere(x, y, z, r))

print("blocks:")
for block in blocks:
    print(block.x, block.y, block.z, block.r)

result = compute(m, blocks)

print("m:")
print(m, "\n")
print("\nspheres:")
for sphere in result:
    print(sphere.x, sphere.y, sphere.z, sphere.r)

# plot(result, bks3, None)
