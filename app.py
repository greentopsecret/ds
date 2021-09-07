#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import argparse

SOURCE_FILE = './datapoints.csv'

def calculate_y(slope, intercept, x):
    return slope * x + intercept

def calculate_mse(data, slope, intercept):
    mse = 0
    for point in data:
        mse += (calculate_y(slope, intercept, point[0]) - point[1]) ** 2
    if args.verbose:
        print('slope: %.2f; intercept: %.2f; mse: %.2f' % (slope, intercept, mse))
    return mse

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--verbose', help='Print debug info', action=argparse.BooleanOptionalAction)
    parser.add_argument('--plot', help='Open plot', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args

args = get_args()

data = genfromtxt(SOURCE_FILE, delimiter=',', skip_header=1)
x = data[:,0]
y = data[:,1]

s = 10
smallest_mse = None
slope = None
intercept = None
while s > 0:
    i = min(y)
    while i < max(y):
        candidate_mse = calculate_mse(data, s, i)
        if smallest_mse is None or smallest_mse > candidate_mse:
            smallest_mse = candidate_mse
            slope = s
            intercept = i
        i += 0.1
    s -= 0.1

print('Smallest MSE: %.2f' % smallest_mse)
print('A (Closest slope): %.2f' % slope)
print('B (Closest intercept): %.2f' % intercept)

if args.plot:
    plt.scatter(x, y)
    plt.plot(
        [min(x), max(x)], 
        [calculate_y(slope, intercept, min(x)), calculate_y(slope, intercept, max(x))], 
        color='gray'
    )
    plt.show()
