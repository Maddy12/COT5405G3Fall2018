import numpy as np
from random import randint
from datetime import datetime
import matplotlib.pyplot as plt


def measure_performance(function, rounds=8, n=1000):
    int_len_list = [2**x for x in np.arange(2, rounds+2)]
    runtimes = dict()
    start_time = datetime.now()
    for int_len in int_len_list:
        end_time = function(int_len, n)
        diff = end_time - start_time
        runtimes[str(int_len)] = diff.microseconds
    plt.plot(int_len_list, runtimes.values())
    plt.xlabel("Int length")
    plt.ylabel("Runtime in microseconds")
    plt.title("Runtime for Multiplying Long Integers")
    plt.show()
    return runtimes


def multiply_no_optimization(int_len, n=1000):
    start = 10L**(int_len-1)  # min value of len int_len
    end = (10L**int_len)-1  # max value of len int_len
    results = randint(start, end)
    for i in range(n-1):
        results = results * randint(start, end)
    return datetime.now()


if __name__ == '__main__':
    measure_performance(function=multiply_no_optimization)