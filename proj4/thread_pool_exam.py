#! /usr/bin/env python3
import queue
import threadpool
import threading
import time


class Printer:
    def print(self, str):
        print(str)


def f1(printer):
    threadlock.acquire()
    printer.print("thread-1")
    threadlock.release()
    time.sleep(1)


def f2(printer):
    threadlock.acquire()
    printer.print("thread-2")
    threadlock.release()
    time.sleep(1)


def f3(printer):
    threadlock.acquire()
    printer.print("thread-3")
    threadlock.release()
    time.sleep(1)


def f4(printer):
    threadlock.acquire()
    printer.print("thread-4")
    threadlock.release()
    time.sleep(1)


threadlock = threading.Lock()
printer = Printer()

pool = threadpool.ThreadPool(4)
req1 = threadpool.WorkRequest(f1, (printer,))
req2 = threadpool.WorkRequest(f2, (printer,))
req3 = threadpool.WorkRequest(f3, (printer,))
req4 = threadpool.WorkRequest(f4, (printer,))
reqs = [req1, req2, req3, req4]

for i in range(5):
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    print("thread end")
