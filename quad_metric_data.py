
# Data for learning a quadratic metric
# You should use X, Y, d as well as X_test, Y_test, d_test

import numpy as np
from scipy import linalg as la
from cvxpy import *
np.random.seed(8)

n = 5 # Dimension
N = 100 # Number of sample
N_test = 10 # Samples for test set

X = np.random.randn(n,N)
Y = np.random.randn(n,N)

X_test = np.random.randn(n,N_test)
Y_test = np.random.randn(n,N_test)

P = np.random.randn(n,n)
P = P.dot(P.T) + np.identity(n)
sqrtP = la.sqrtm(P)

d = np.linalg.norm(sqrtP.dot(X-Y),axis=0)
d = np.maximum(d+np.random.randn(N),0)
d_test = np.linalg.norm(sqrtP.dot(X_test-Y_test),axis=0)
d_test = np.maximum(d_test+np.random.randn(N_test),0)

ones = np.ones((1, N))
P = Semidef(n)
d_sq = (X - Y).T * P * (X - Y)
d_diag = diag(d_sq)
obj = Minimize(1.0/N * (sum_entries(square(d - d_diag))))
cons = []
prob = Problem(obj, cons)
prob.solve()
print "Optimal value for d:", prob.value

# d_test
print "Optimal value for d_test:", 1.0/N_test * (np.sum(np.square(d_test - np.diag((X_test - Y_test).T * P.value * (X_test - Y_test)))))
