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
    # int_len_list = [512, 1024]  # This is test code to jump to the size 512 test
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
    This function multiplies two random signed integers based on a passed integer length.
    It multiplies two random values 1000 times and records each runtime where then the maximum and average are calculated.
    :param int_len: Length of integer
    :param n: Rounds to multiply, new random integers are initialized each run.
    :return:
    """
    try:
        int_len = int(int_len)
        start_neg = -(10**int_len)+1
        end_neg = -(10**(int_len-1))
        start_pos = 10**(int_len-1)
        end_pos = (10**int_len)-1  # max value of len int_len
        runtimes = list()
        for i in range(n-1):
            x = choice([randint(start_neg, end_neg), randint(start_pos, end_pos)])
            y = choice([randint(start_neg, end_neg), randint(start_pos, end_pos)])
            start_time = time()
            a, b, sign = strip_signs(x, y)
            results = multiply_by_digit(a, b, sign)
            end_time = time()
            print(results)
            diff = end_time - start_time
            runtimes.append(diff)
        return np.mean(runtimes), np.max(runtimes)
    except:
        import pdb;pdb.set_trace()


def strip_signs(a, b):
    if (a < 0 and b < 0) or (a > 0 and b > 0):
        res_sign = '-'
    else:
        res_sign = '+'
    a = abs(a)
    b = abs(b)
    return a, b, res_sign


def multiply_by_digit(a, b, sign):
    sum_result = x = 0
    while b > 0:
        carry = y = res2sum = shift_y = 0
        a_temp = a
        shift_x = 10**x
        b_lsb = int(b % 10)
        while a_temp > 0:
            shift_y = 10**y
            a_lsb = int(a_temp % 10)
            result = a_lsb * b_lsb + carry
            if result > 9:
                carry = int(result / 10)
                result %= 10
            else:
                carry = 0
            a_temp = int(a_temp / 10)
            # Prev line crashes when number has 512+ digits
            res2sum += result * shift_y
            y += 1
        res2sum += carry * shift_y * 10
        sum_result += res2sum * shift_x
        b = int(b / 10)
        x += 1
    sum_result = int(sign + str(sum_result))
    # print(sum_result)
    return sum_result


if __name__ == '__main__':
    measure_performance(function=multiply_no_optimization)