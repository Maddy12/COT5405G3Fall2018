# -*- coding: utf-8 -*-
"""
Created on Wed Sep  12 23:02:48 2018
@author: Gireesh
"""
# THis program generates two n digit rangom numbers and then divide  first number by second

from random import randint
import random
import time
import matplotlib.pyplot as plt

#creating random integers of N digits
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

#c= a/b; 
#print (z)
#print (c)

  
N=[4, 8, 16, 32, 64, 128, 256, 512]; 
time_for_n_digit=[];
xrange=list(range(1, 1000))
for i in range (0, len(N)):
    t0 = time.perf_counter()
    time_base=0;
    time_for_individual_N=[];
    for j in range(1,1000):
        a=random_with_N_digits(N[i]);
        b=random_with_N_digits(N[i]); 
        t0 = time.perf_counter()
        c=a*b;
        t1 = time.perf_counter()
        total_n = t1-t0; # this is the time taken for the specific operation above
        time_for_individual_N.append(total_n);       
        time_base=time_base+total_n; # adding the time over the operations 1-1000
    plt.figure();
    plt.plot(xrange, time_for_individual_N)
    if (N[i]<129): # this is to provide different y -scale ranges
        plt.ylim((-0.00000025, 0.000001)) 
        plt.xlabel('attempt of operation')
        plt.ylabel('time taken for execution')
    else:
        plt.ylim((-0.00000025, 0.00001)) 
        plt.xlabel('attempt of operation')
        plt.ylabel('time taken for execution')
        
    plt.title('Performance of multiplication for: n= %i' %N[i],fontsize=14, color='red')
        
    time_for_n_digit.append(time_base);
  
print(time_for_n_digit)    
# plotting the performance in terms of time used against the digits    
plt.figure();
plt.plot(N, time_for_n_digit)
plt.xlabel('number of digits')
plt.ylabel('time taken for execution')
plt.title('Performance of multiplication',fontsize=14, color='red')


# Optional: Plotting in logarithmic scale
#plt.figure();
#plt.plot(N, time_for_n_digit)
#plt.yscale('log')
#plt.xlabel('number of digits')
#plt.ylabel('time taken for execution')
#plt.title('Performance of multiplication in logarithmic scale',fontsize=14, color='red')
