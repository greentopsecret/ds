import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

def calculate_y(slope, intercept, x):
    return slope * x + intercept

def calculate_mse(data, slope, intercept):
    mse = 0
    for point in data:
        mse += (calculate_y(slope, intercept, point[0]) - point[1]) ** 2
    print('slope: %.2f; intercept: %.2f; mse: %.2f' % (slope, intercept, mse))
    return mse

name = './datapoints.csv'
data = genfromtxt(name, delimiter=',', skip_header=1)
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

plt.scatter(x, y)
plt.plot(
    [min(x), max(x)], 
    [calculate_y(slope, intercept, min(x)), calculate_y(slope, intercept, max(x))], 
    color='gray'
)
plt.show()
