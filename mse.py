#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import argparse
import sys

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
    parser.add_argument('--source', help='Source file', default='./datapoints.csv')
    parser.add_argument('--verbose', help='Print debug info', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args

args = get_args()

try:
    data = genfromtxt(args.source, delimiter=',', skip_header=1)
except:
    print('Cannot read data from the file "%s"' % args.source)
    sys.exit(1)

x = data[:,0]
y = data[:,1]

slope = 10
smallest_mse = None
closest_slope = None
closest_intercept = None
while slope > 0:
    intercept = max(y)
    previous_candidate_mse = None
    while intercept > min(y):
        candidate_mse = calculate_mse(data, slope, intercept)

        # Optimisation: we don't need to continue if mse is growing
        if (previous_candidate_mse is not None and previous_candidate_mse < candidate_mse):
            break

        if smallest_mse is None or smallest_mse > candidate_mse:
            smallest_mse = candidate_mse
            closest_slope = slope
            closest_intercept = intercept
        intercept -= 0.1
        previous_candidate_mse = candidate_mse
    slope -= 0.1

plt.scatter(x, y)
plt.plot(
    [min(x), max(x)],
    [calculate_y(slope, closest_intercept, min(x)), calculate_y(closest_slope, closest_intercept, max(x))],
    color='gray'
)
plt.show()

print('Smallest MSE: %.2f' % smallest_mse)
print('A (Closest slope): %.2f' % closest_slope)
print('B (Closest intercept): %.2f' % closest_intercept)