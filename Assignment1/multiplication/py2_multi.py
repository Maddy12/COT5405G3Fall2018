import numpy as np
from random import randint, choice
from time import time
import matplotlib.pyplot as plt

author = "Madeline Schiappa, Jack P. Oakley, Elakkat Gireesh, Shah Hassan"
author_email = "madelineschiappa@knights.ucf.edu, jack.p.oakley@knights.ucf.edu, elakkat@knights.ucf.edu, shahhassan@knights.ucf.edu"


def measure_performance(function, rounds=8, n=1000):
    """
    This function will measure the performance of a passed function.

    :param function: The function is required to output an avg_runtime and a max_runtime for whatever tasks it is performing.
    :param rounds: Number of int sizes to iterate through starting at 2**2 = 4
    :param n: Number of runs per int size.
    :return:
    """
    int_len_list = [2**x for x in np.arange(2, rounds+2)]
    avg_runtimes = list()
    max_runtimes = list()
    for int_len in int_len_list:
        avg_runtime, max_runtime = function(int_len, n)
        avg_runtimes.append(avg_runtime)
        max_runtimes.append(max_runtime)
    plt.plot(int_len_list, avg_runtimes)
    plt.plot(int_len_list, max_runtimes)
    plt.legend(['Average Runtime', 'Max Runtime'], loc='upper left')
    plt.xlabel("Integer Size")
    plt.ylabel("Runtime in microseconds")
    plt.title("Runtime for Multiplying Long Integers")
    plt.show()


def multiply_no_optimization(int_len, n=1000):
    """
    This function multiplys two random signed integers based on a passed integer length.
    It multiplys two random values 1000 times and records each runtime where then the maximum and average are calculated.
    :param int_len: Length of integer
    :param n: Rounds to multiply, new random integers are initialized each run.
    :return:
    """
    start_neg = -(10L**int_len)+1
    end_neg = -(10L**(int_len-1))
    start_pos = 10L**(int_len-1)
    end_pos = (10L**int_len)-1  # max value of len int_len
    runtimes = list()
    for i in range(n-1):
        x = choice([randint(start_neg, end_neg), randint(start_pos, end_pos)])
        y = choice([randint(start_neg, end_neg), randint(start_pos, end_pos)])
        start_time = time()
        results = x*y
        end_time = time()
        diff = end_time - start_time
        runtimes.append(diff)
    return np.mean(runtimes), np.max(runtimes)


if __name__ == '__main__':
    measure_performance(function=multiply_no_optimization)