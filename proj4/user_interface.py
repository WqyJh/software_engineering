#!/usr/bin/env python3
import sys


def print_usage():
    print("Hello friend, this software can help you to calculate how to put m balloons")
    print("in a 3D-box area bounded by [-1, 1], and maximize the sum of r square\n")
    print("Useage:")
    print("-h --help", "print this document")
    print("-f --file", "provide a file that contains input data")
    print("         ", "with a number m in first line indicate the number of balloons")
    print("         ", "and a number n in the second line indicate the number of blocks")
    print("         ", "in the following n lines is the specified coordinate of these blocks")
    print("         ", "in the order of x, y, z, r, and divided by empty character")
    print("\nNow, enjoy it")
    print("The result would be print in the screen, which is the coordinate of the balloons")
    print("in the order of x, y, z, r, and divided by one space character")

def read_data():
    filename = sys.argv[2]
    f = open(filename)

    m = int(f.readline().strip())
    n = int(f.readline().strip())

    data = []
    for i in range(n):
        data.append([float(x) for x in f.readline().split()])
    f.close()
    return (m, data)

def start():
    if len(sys.argv) < 3:
        print_usage()
        return None
    return read_data()


