from satisfy_some_constraints_data import *
import numpy as np
import cvxpy as cp
import collections

ones = np.ones((m, 1))
q = cp.Variable(m)
x = cp.Variable(n)
mu = cp.Variable()

c = np.asmatrix(c).T
b = np.asmatrix(b).T

obj = cp.Minimize(c.T * x)
cons = [cp.sum_entries(q) <= (m - k) * mu, q >= 0, mu > 0]
cons += [A * x - b + mu * ones <= q]

prob = cp.Problem(obj, cons)
prob.solve()

print "lambda:" ,1.0 / mu.value
print "Objective value:", prob.value
x_star = x.value
satisfied = 0
consdict = {}
for i in xrange(m):
    y = (np.dot(A[i, :], x_star)[0, 0] - b[i])[0, 0]
    if y <= 1e-6:
        satisfied += 1
        consdict[y] = i

print "Constraints satisfied:", satisfied

# Find the k constraints with the smallest value
od = collections.OrderedDict(sorted(consdict.items()))
ind = []
temp = 0
for ele in od.values():
    ind.append(ele)
    temp += 1
    if temp >= k:
        break

A_hat = A[ind, :]
b_hat = b[ind, :]

x = cp.Variable(n)
prob = cp.Problem(cp.Minimize(c.T * x), [A_hat * x <= b_hat])
prob.solve()
print "Objective value with k constraints:", prob.value
