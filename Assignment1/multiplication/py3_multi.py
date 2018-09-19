import numpy as np
import os
from random import randint, choice
from time import time
import seaborn as sns
import matplotlib.pyplot as plt

author = "Madeline Schiappa, Jack P. Oakley, Elakkat Gireesh, Shah Hassan"
author_email = "madelineschiappa@knights.ucf.edu, jack.p.oakley@knights.ucf.edu, elakkat@knights.ucf.edu, shahhassan@knights.ucf.edu"


def measure_performance(algorithm, rounds=8, n=1000, max_rt=False, log=False):
    """
    This function will measure the performance of a passed function.

    :param algorithm: The algorithm used to run the multiplication task.
    :param rounds: Number of int sizes to iterate through starting at 2**2 = 4
    :param n: Number of runs per int size.
    :return:
    """
    int_len_list = [2**x for x in np.arange(2, rounds+2)]
    # int_len_list = [4, 8, 32]  # This is test code to jump to the size 512 test
    save_dir = os.getcwd()
    avg_runtimes = list()
    max_runtimes = list()
    runtimes_dict = dict()
    for int_len in int_len_list:
        avg_runtime, max_runtime, runtimes = multiply_simulation(int_len, algorithm, n)
        runtimes_dict[str(int_len) + "_digits"] = runtimes
        avg_runtimes.append(avg_runtime)
        max_runtimes.append(max_runtime)
        sns.distplot(runtimes, kde_kws={'label' : 'KDE'})
        plt.xlabel("Runtime in microseconds")
        plt.ylabel("Kernel Density Estimate")
        plt.title("Runtime Distribution for " + str(int_len))
        plt.savefig(os.path.join(save_dir, str(int_len) + "_digits"))
        plt.close()
    plot_avg_runtime(int_len_list, avg_runtimes, max_runtimes, save_dir, log=False, max_rt=False)
    plot_avg_runtime(int_len_list, avg_runtimes, max_runtimes, save_dir, log=True, max_rt=False)


def plot_avg_runtime(int_len_list, avg_runtimes, max_runtimes, save_dir, log=False, max_rt=False):
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    plt.plot(int_len_list, avg_runtimes)
    if max_rt:
        plt.plot(int_len_list, max_runtimes)
        plt.legend(['Average Runtime', 'Max Runtime'], loc='upper left')
    if log:
        ax.set_yscale("log", nonposy='clip')
        plt.ylabel("Log Runtime in microseconds")
        save_name = os.path.join(save_dir, 'avg_log_runtime.png')
    else:
        plt.ylabel("Runtime in microseconds")
        save_name = os.path.join(save_dir, 'avg_runtime.png')
    plt.xlabel("Integer Size")
    plt.title("Runtime for Multiplying Long Integers")
    plt.savefig(save_name, dpi=300)
    plt.close()


def multiply_simulation(int_len, algorithm, n=1000):
    """
    This function multiplies two random signed integers based on a passed integer length.
    It multiplies two random values 1000 times and records each runtime where then the maximum and average are calculated.
    :param int_len: Length of integer
    :param algorithm: algorithm to run with inputs x and y
    :param n: Rounds to multiply, new random integers are initialized each run.
    :return:
    """
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
        results = algorithm(x, y)
        end_time = time()
        diff = end_time - start_time
        runtimes.append(diff)
    return np.mean(runtimes), np.max(runtimes), runtimes


def python_optimization(x, y):
    return x*y


def strip_signs(a, b):
    """
    This function strips the signs off of the signed integers and returns their absolute value as well as determines
    the sign that will be on the resulting product and returns it.
    :param a: The first signed number input
    :param b: The second signed number input
    :return: Absolute value of a, Absolute value of b, Resulting sign from product
    """
    if (a < 0 and b < 0) or (a > 0 and b > 0):
        res_sign = -1
    else:
        res_sign = 1
    a = abs(a)
    b = abs(b)
    return a, b, res_sign


def multiply_by_digit(x, y):
    """
    This function takes two unsigned integers and goes digit by digit to multiply each digit starting from the LSB by
    making use of a carry digit and then adds the resulting multiplications together to get an end result of the product
    of the two integers.  It then attaches the passed in sign to return a properly signed product.
    :param x: First integer to be multiplied
    :param y: Second integer to be multiplied
    :return: Product of a and b with proper sign
    """
    a, b, sign = strip_signs(x, y)
    x = sum_result = 0
    y = 0
    while b > 0:
        carry = y = res2sum = shift_y = 0
        a_temp = a
        shift_x = 10**x
        b_lsb = b % 10
        while a_temp > 0:
            shift_y = 10**y
            a_lsb = a_temp % 10
            result = a_lsb * b_lsb + carry
            if result > 9:
                carry = result // 10
                result %= 10
            else:
                carry = 0
            a_temp = a_temp // 10
            res2sum += result * shift_y
            y += 1
        res2sum += carry * shift_y * 10
        sum_result += res2sum * shift_x
        b = b // 10
        x += 1
    sum_result = sign * sum_result
    return sum_result


if __name__ == '__main__':
    measure_performance(algorithm=multiply_by_digit, log=True)