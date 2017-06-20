#!/usr/bin/env python3
import multiprocessing
import time

class Printer(object):

    def print(self, msg):
        print("Printer", msg)


def f1(printer):
    time.sleep(2)
    printer.print("f1")
    return 1


def f2(printer):
    time.sleep(2)
    printer.print("f2")
    return 2


def f3(printer):
    time.sleep(2)
    printer.print("f3")
    return 3


def f4(printer):
    time.sleep(2)
    printer.print("f4")
    return 4


pool = multiprocessing.Pool(4)
result = []
printer = Printer()

for i in range(5):
    result.clear()
    result.append(pool.apply_async(f1, (printer, )))
    result.append(pool.apply_async(f2, (printer, )))
    result.append(pool.apply_async(f3, (printer, )))
    result.append(pool.apply_async(f4, (printer, )))

    print("before")
    for res in result:
        print("res", res.get())
    print("end\n")

pool.close()
pool.join()
