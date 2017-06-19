#!/usr/bin/env python2

from ivisual import *

def plot(result, blocks, name):
    scene = canvas(title='3D scene')

    for block in blocks:
        sphere(pos=vector(block.x, block.y, block.z), radius=1.0 / 50, color=color.red)

    for sph in result:
        sphere(pos=vector(sph.x, sph.y, sph.z), radius=sph.r, color=color.blue)

    box(pos=vector(0, 0, 0), size=(2, 2, 2), color=color.blue, opacity=0.2)