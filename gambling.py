import numpy as np
from cvxpy import *

n = 5
m = 5
p = np.array([[0.5], [0.6], [0.6], [0.6], [0.2]])
p = np.asmatrix(p)
q = np.array([[10.], [5.], [5.], [20.], [10.]])
q = np.asmatrix(q)
S = np.array([[1., 0., 1., 0., 0.], [1., 0., 0., 1., 0.], [0., 0., 0., 0., 1.], [0., 1., 1., 0., 0.], [0., 0., 1., 1., 0.]])

x = Variable(n)
y = Variable(1)
obj = Minimize(-x.T * p + y)
cons = [S * x <= y * np.ones((m, 1)), x >= 0, x <= q]
prob = Problem(obj, cons)
prob.solve()
opt_wc = -prob.value

y = Variable()
obj = Minimize(-q.T * p + y)
cons = [S * q <= y * np.ones((m, 1))]
prob = Problem(obj, cons)
prob.solve()
wc = -prob.value

lam = Variable(m)
a = Variable(n)
b = Variable(n)
obj = Minimize(a.T * q)
cons = [-p + S.T * lam + a - b == 0, sum(lam) == 1, lam >= 0, a >= 0, b >= 0]
prob = Problem(obj, cons)
prob.solve()

print opt_wc
print wc
print lam.value
