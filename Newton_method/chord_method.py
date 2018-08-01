'''
    Pure Python/Numpy implementation of the BFGS algorithm.
    Reference: https://en.wikipedia.org/wiki/Broyden%E2%80%93Fletcher%E2%80%93Goldfarb%E2%80%93Shanno_algorithm
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import numpy.linalg as ln
import scipy as sp
import scipy.optimize
from copy import deepcopy
import time
import random

# Objective function
def f(x):
    return (x[0]**2-1)**2#x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 6*x[1] + 20


# Derivative
def f1(x):
    return np.array([2 * x[0] - x[1] + 9, -x[0] + 2*x[1] - 6])


def chords_method(f, fprime, x0, maxiter=None, epsi=10e-3):
    it = 0
    roots = [random.randint(-10,10) for i in range(len(x0))] 
    prev_roots = [0 for i in range(len(x0))]
    new_roots = [0 for i in range(len(x0))]


    while f(roots) > epsi:
        for i in range(len(roots)):
            new_roots[i] = roots[i] - \
             f(roots)*((roots[i]-prev_roots[i])/(f(roots) - f(prev_roots)))
        prev_roots = deepcopy(roots)
        roots = deepcopy(new_roots)
        print(abs(f(roots) - epsi))
        time.sleep(1)
        it+=1
    return roots, it


result, k = chords_method(f, f1, np.array([1]))

print('Result of chords method:')
print('Final Result (best point): %s' % (result))
print('Iteration Count: %s' % (k))