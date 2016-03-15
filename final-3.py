from zero_crossings_data import *
import numpy as np
import cvxpy as cp
import math
import numpy.linalg as la
import matplotlib.pyplot as plt

s_d = np.diag(s)
cos_m = np.zeros((n, B))
sin_m = np.zeros((n, B))
for i in xrange(n):
    for j in xrange(B):
        cos_m[i, j] = math.cos(2 * math.pi/n * (f_min + j) * (i + 1))
        sin_m[i, j] = math.sin(2 * math.pi/n * (f_min + j) * (i + 1))

y_v = cp.Variable(n)
p = cp.Variable(n)
a = cp.Variable(B)
b = cp.Variable(B)
obj = cp.Minimize(cp.norm(y_v))
cons = [y_v == cos_m * a + sin_m * b, y_v == s_d * p, p >= 0, cp.sum_entries(p) == n]
prob = cp.Problem(obj, cons)
prob.solve()

y_hat = y_v.value
line1, = plt.plot(range(1, n + 1), y)
line2, = plt.plot(range(1, n + 1), y_hat)
plt.xlabel('$t$')
plt.ylabel('$y$')
plt.legend([line1, line2], ["$y$", "$\hat{y}$"], loc = 1)
plt.show()

y = np.asmatrix(y).T
print "Relative recovery error:", la.norm(y_hat - y, 2) / la.norm(y, 2)
