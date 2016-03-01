import numpy as np
#from cvxpy import *
import matplotlib.pyplot as plt
import numpy.linalg as la

p = 100
n = 500

# feasible
A = np.random.rand(p, n) * 2 - 1
A[0, :] = np.maximum(np.absolute(A[0, :]), 0.01)
print A
b = np.dot(A, np.random.rand(n, 1))
c = np.random.rand(n, 1) * 2 - 1
x0 = np.random.rand(n, 1)
nu0 = np.zeros((p, 1))

# # infeasible
# A = np.random.rand(p, n)
# b = -A * ones((n, 1))
#
# # unbounded
# A[:, 0] = 0
# b(1) = 0
# c(1) = -1

assert(la.matrix_rank(A) == p)
assert(x0.all() > 0)

def f(x):
    return np.dot(c.T, x) - np.sum(np.log(x))

def grad_f(x):
    return c - 1.0/x

def H_f(x):
    return np.diag(np.square(1.0/x)[:, 0])

def H_inv_f(x):
    return np.diag(np.square(x)[:, 0])

# residual
def r_dual(x, nu):
    return grad_f(x) + np.dot(A.T, nu)

def r_pri(x):
    return np.dot(A, x) - b

def r(x, nu):
    return np.vstack((r_dual(x, nu), r_pri(x)))[:, 0]

# Newton's method parameters
alpha = 0.8
beta = 0.9
epsilon = 1e-6
maxiter = 50

x = x0
nu = nu0
residuals = [la.norm(r(x, nu))]
solved_status = False
for k in xrange(maxiter):
    H_inv = H_inv_f(x)
    g = grad_f(x)
    w = -la.solve(np.dot(np.dot(A, H_inv), A.T), np.dot(np.dot(A, H_inv), g) - np.dot(A, x) + b)
    dx = -np.dot(H_inv, g + np.dot(A.T, w))
    dnu = w - nu
    t = 1
    while((x + t * dx).any() <= 0 or la.norm(r(x + t * dx, nu + t * dnu)) > (1 - alpha * t) * residuals[-1]):
        t = beta * t
    x = x + t * dx
    nu = nu + t * dnu
    residuals.append(la.norm(r(x, nu)))
    print la.norm(r(x, nu))
    if residuals[-1] <= epsilon:
        solved_status = True
        break

print solved_status
