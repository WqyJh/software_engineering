#!/usr/bin/env python

import ivisual

def plot(result, blocks, name):
    scene = ivisual.canvas(title='3D scene')

    for block in blocks:
        ivisual.sphere(pos=vector(block.x, block.y, block.z), radius=1.0 / 50, color=ivisual.color.red)

    for sphere in result:
        ivisual.sphere(pos=vector(sphere.x, sphere.y, sphere.z), radius=sphere.r, color=ivisual.color.blue)

    ivisual.box(pos=vector(0, 0, 0), size=(2, 2, 2), color=ivisual.color.blue, opacity=0.2)