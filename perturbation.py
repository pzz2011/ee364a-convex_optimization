import numpy as np
from cvxpy import *

Q = np.matrix([[1, -0.5], [-0.5, 2]])
f = np.matrix([[-1], [0]])
a1 = np.array([1, 2])
a2 = np.array([1, -4])
a3 = np.array([5, 76])


x = Variable(2)

constraints = [a1 * x <= -2, a2 * x <= -3, a3 * x <= 1]
obj = Minimize(quad_form(x, Q) + f.T * x)
prob = Problem(obj, constraints)

prob.solve()
print x.value
print prob.value
print constraints[0].dual_value
print constraints[1].dual_value
print constraints[2].dual_value

pstar = prob.value
l1 = constraints[0].dual_value
l2 = constraints[1].dual_value

delta1 = [-0.01, 0, 0.01]
delta2 = [-0.01, 0, 0.01]

for d1 in delta1:
    for d2 in delta2:
        u1 = -2 + d1
        u2 = -3 + d2
        x = Variable(2)
        constraints = [a1 * x <= u1, a2 * x <= u2, a3 * x <= 1]
        obj = Minimize(quad_form(x, Q) + f.T * x)
        prob = Problem(obj, constraints)
        prob.solve()
        pexact = prob.value
        print ' '
        print d1, d2, pstar - l1 * d1 - l2 * d2, pexact
