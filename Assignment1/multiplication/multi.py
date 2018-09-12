import numpy as np
from random import randint
from time import time
import matplotlib.pyplot as plt


def measure_performance(function, rounds=8, n=1000):
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
    plt.ylabel("Runtime in microseconds")
    plt.title("Runtime for Multiplying Long Integers")
    plt.show()


def multiply_no_optimization(int_len, n=1000):
    start_neg = -(10L**int_len)+1
    end_neg = -(10L**(int_len-1))
    start_pos = 10L**(int_len-1)
    end_pos = (10L**int_len)-1  # max value of len int_len
    runtimes = list()
    for i in range(n-1):
        if randint(1, 2) == 1:
            x = randint(start_pos, end_pos)
        else:
            x = randint(start_neg, end_neg)
        if randint(1, 2) == 1:
            y = randint(start_pos, end_pos)
        else:
            y = randint(start_neg, end_neg)
        start_time = time()
        results = x*y
        print(results)
        end_time = time()
        diff = end_time - start_time
        runtimes.append(diff)
    return np.mean(runtimes), np.max(runtimes)


if __name__ == '__main__':
    measure_performance(function=multiply_no_optimization)