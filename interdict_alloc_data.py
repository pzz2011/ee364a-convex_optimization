import numpy as np
from cvxpy import *
from math import *

np.random.seed(0)
(n, m) = (10, 20)
edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 5), \
         (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (4, 7), \
         (5, 6), (5, 7), (6, 7), (6, 8), (6, 9), (7, 8), \
         (7, 9), (8, 9)]
a = 2*np.random.rand(m, 1)
x_max = 1+np.random.rand(m, 1)
B = m/2.0
a2 = np.diag(a[:, 0])

A = np.zeros((n, m))
for k in xrange(len(edges)):
    i1 = edges[k][0]
    i2 = edges[k][1]
    A[i1, k] = -1
    A[i2, k] = 1

x = Variable(m)
z = Variable(n)
obj = Minimize(z[n-1])
cons = [z[0] == 0, A.T * z >= -a2 * x, x >= 0, x <= x_max, sum_entries(x) <= B]
prob = Problem(obj, cons)
prob.solve()
print "Optimal detection failure:", exp(prob.value)

x_unif = B/m * np.ones((m, 1))
z_unif = Variable(n)
obj = Minimize(z_unif[n - 1])
ax = np.dot(-a2, x_unif)
cons = [z_unif[0] == 0, A.T * z_unif >= ax]
prob = Problem(obj, cons)
prob.solve()
print "Optimal with uniform allocation:", exp(prob.value)
