import numpy as np
import cvxpy as cp
from matrix_equilibration_data import *
import numpy.linalg as la

B = np.square(A)

u = cp.Variable(m)
v = cp.Variable(n)
Be = 0
for i in xrange(m):
    for j in xrange(n):
        Be += cp.exp(cp.log(B[i, j]) + u[i] + v[j])
obj = cp.Minimize(Be)
cons = [cp.sum_entries(u) == 1, cp.sum_entries(v) == 1]
prob = cp.Problem(obj, cons)
prob.solve()

D = np.zeros((m, m))
for i in xrange(m):
    D[i, i] = np.exp(u.value[i, 0] / p)

E = np.zeros((n, n))
for i in xrange(n):
    E[i, i] = np.exp(v.value[i, 0] / p)

A_equi = np.dot(np.dot(D, A), E)
print "2-norm for every row:"
for i in xrange(m):
    print la.norm(A_equi[i, :])

print "2-norm for every column:"
for j in xrange(n):
    print la.norm(A_equi[:, j])
