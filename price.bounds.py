import numpy as np
from cvxpy import *

m = 200
r = 1.05
S_0 = 1
S = np.linspace(0.5, 2, 200).T
F = 0.9
C = 1.15

V = np.zeros((m, 7))
V[:, 0] = r
V[:, 1] = S
V[:, 2] = np.maximum(0, S - 1.1)
V[:, 3] = np.maximum(0, S - 1.2)
V[:, 4] = np.maximum(0, 0.8 - S)
V[:, 5] = np.maximum(0, 0.7 - S)
V[:, 6] = np.maximum(F, np.minimum(C, S)) - S_0
P = np.array([1, S_0, 0.06, 0.03, 0.02, 0.01])
P = np.asmatrix(P).T

collar = Variable()
y = Variable(m)
obj = Minimize(collar)
cons = [y >= 0, V[:, 0:6].T * y == P, V[:, 6].T * y == collar]
prob = Problem(obj, cons)
prob.solve()
print prob.status
print "p collar min:", collar.value

collar = Variable()
y = Variable(m)
obj = Maximize(collar)
cons = [y >= 0, V.T[0:6, :] * y == P, V.T[6, :] * y == collar]
prob = Problem(obj, cons)
prob.solve()

print "p collar max", collar.value
