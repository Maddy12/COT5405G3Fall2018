import numpy as np
from random import randint
from time import time
import matplotlib.pyplot as plt


def measure_performance(function, rounds=8, n=1000, type='avg'):
    int_len_list = [2**x for x in np.arange(2, rounds+2)]
    runtimes = dict()
    for int_len in int_len_list:
        avg_runtime = function(int_len, n)
        runtimes[str(int_len)] = avg_runtime
    plt.plot(int_len_list, runtimes.values())
    plt.xlabel("Integer Size")
    plt.ylabel("Runtime in microseconds".format(type))
    plt.title("Runtime for Multiplying Long Integers")
    plt.show()
    return runtimes


def avg_multiply_no_optimization(int_len, n=1000):
    start = 10L**(int_len-1)  # min value of len int_len
    end = (10L**int_len)-1  # max value of len int_len
    runtimes = list()
    for i in range(n-1):
        start_time = time()
        results = randint(start, end) * randint(start, end)
        print(results)
        end_time = time()
        diff = end_time - start_time
        runtimes.append(diff)
    return np.mean(runtimes)


def max_multiply_no_optimization(int_len, n=1000):
    start = 10L**(int_len-1)  # min value of len int_len
    end = (10L**int_len)-1  # max value of len int_len
    runtimes = list()
    for i in range(n-1):
        start_time = time()
        results = randint(start, end) * randint(start, end)
        print(results)
        end_time = time()
        diff = end_time - start_time
        runtimes.append(diff)
    return np.max(runtimes)


if __name__ == '__main__':
    measure_performance(function=avg_multiply_no_optimization)
    measure_performance(function=max_multiply_no_optimization, type='max')
    plt.legend(['avg', 'max'], loc='upper left')