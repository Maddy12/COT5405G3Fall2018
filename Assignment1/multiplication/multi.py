import numpy as np
from random import randint
from time import time
import matplotlib.pyplot as plt


def measure_performance(function, rounds=8, n=1000, type='avg'):
    int_len_list = [2**x for x in np.arange(2, rounds+2)]
    avg_runtimes = list()
    max_runtimes = list()
    for int_len in int_len_list:
        avg_runtime, max_runtime = function(int_len, n)
        avg_runtimes.append(avg_runtime)
        max_runtimes.append(max_runtime)
    plt.plot(int_len_list, avg_runtimes)
    plt.plot(int_len_list, max_runtimes)
    plt.legend(['avg', 'max'], loc='upper left')
    plt.xlabel("Integer Size")
    plt.ylabel("Runtime in microseconds".format(type))
    plt.title("Runtime for Multiplying Long Integers")
    plt.show()


def avg_multiply_no_optimization(int_len, type, n=1000):
    #start = 10L**(int_len-1)  # min value of len int_len
    start = -(10L**int_len)+1
    end = (10L**int_len)-1  # max value of len int_len
    runtimes = list()
    for i in range(n-1):
        start_time = time()
        results = randint(start, end) * randint(start, end)
        print(results)
        end_time = time()
        diff = end_time - start_time
        runtimes.append(diff)
    return np.mean(runtimes), np.max(runtimes)


def max_multiply_no_optimization(int_len, n=1000):
    start = -(10L**int_len)-1  # min value of len int_len
    end = (10L**int_len)-1  # max value of len int_len
    runtimes = list()
    for i in range(n-1):
        x = randint(start, end)
        y = randint(start, end)
        start_time = time()
        results =  x*y
        print(results)
        end_time = time()
        diff = end_time - start_time
        runtimes.append(diff)
    return np.max(runtimes)


if __name__ == '__main__':
    measure_performance(function=avg_multiply_no_optimization)