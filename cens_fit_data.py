import numpy as np
import numpy.linalg as la
from cvxpy import *
# data for censored fitting problem.
np.random.seed(15)

n = 20;  # dimension of x's
M = 25;  # number of non-censored data points
K = 100; # total number of points
c_true = np.random.randn(n,1)
X = np.random.randn(n,K)
y = np.dot(np.transpose(X),c_true) + 0.1*(np.sqrt(n))*np.random.randn(K,1)

# Reorder measurements, then censor
sort_ind = np.argsort(y.T)
y = np.sort(y.T)
y = y.T
X = X[:, sort_ind.T]
D = (y[M-1]+y[M])/2.0
y = y[range(M)]

c = Variable(n)
y_hat = Variable(K)
obj1 = Minimize(norm(y_hat - X.T * c))
cons1 = [y_hat[0:M] == y, y_hat[M:K] >= D]
prob1 = Problem(obj1, cons1)
prob1.solve()
c_hat = c.value
err_hat = la.norm(c_true - c_hat, 2) / la.norm(c_true, 2)

c = Variable(n)
obj2 = Minimize(norm(y - X[:, 0:M].T * c))
cons2 = []
prob2 = Problem(obj2, cons2)
prob2.solve()
c_ls = c.value
err_ls = la.norm(c_true - c_ls, 2) / la.norm(c_true, 2)

print "c_hat:"
print c_hat
print "c_ls"
print c_ls
print "err_hat:", err_hat
print "err_ls", err_ls
