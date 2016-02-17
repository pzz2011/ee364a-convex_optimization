import numpy as np
from cvxpy import *

n = 4
x = np.array([[0.1], [0.2], [-0.05], [0.1]])
S_diag = np.zeros((4, 4))
S_diag[0, 0] = 0.2
S_diag[1, 1] = 0.1
S_diag[2, 2] = 0.3
S_diag[3, 3] = 0.1

S = Semidef(n)
obj = Minimize(- x.T * S * x)
cons = []
for i in xrange(4):
    cons.append(S[i, i] == S_diag[i, i])
cons.append(S[0, 1] >= 0)
cons.append(S[0, 2] >= 0)
cons.append(S[1, 2] <= 0)
cons.append(S[1, 3] <= 0)
cons.append(S[2, 3] >= 0)

prob = Problem(obj, cons)
prob.solve()
S_wc = S.value
var_wc = -prob.value
var_diag = np.dot(np.dot(x.T, S_diag), x)
print "Covariance matrix:"
print S_wc
print "Worst-case risk:", var_wc
print "Risk obtained when S is diagonal:", var_diag[0, 0]
