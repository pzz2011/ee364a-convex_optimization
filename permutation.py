import numpy as np
import numpy.linalg as la
from ls_perm_meas_data import *
from cvxpy import *

P_hat = np.eye(m)
#tolrance
tol = 10e-6

#Estimate when P = I
x = Variable(n)
Py = np.dot(P_hat.T, y)
obj = Minimize(norm(A * x - Py))
prob = Problem(obj, [])
prob.solve()
x_0 = x.value
err = prob.value

#Heuristic method
while 1:
    prev_err = err

    # Given P_hat, find x_hat that minimize err
    x = Variable(n)
    Py = np.dot(P_hat.T, y)
    obj = Minimize(norm(A * x - Py, 1))
    prob = Problem(obj, [])
    prob.solve()
    x_hat = x.value

    # Given x_hat find P_hat that minimize err
    Ax = np.dot(A, x_hat)
    residuals = {}
    for i in xrange(m):
        residuals[(Ax[i, 0] - y[i, 0])**2] = i
    rkeys = sorted(residuals, reverse = True)
    xis = {}
    yis = {}
    k_track = 0
    for key in rkeys:
        idx = residuals[key]
        xis[Ax[idx, 0]] = idx
        yis[y[idx, 0]] = idx
        k_track = k_track + 1
        if k_track == k:
            break
    xi = sorted(xis)
    yi = sorted(yis)
    P_hat = np.eye(m)
    for i in xrange(k):
        P_hat[yis[yi[i]], yis[yi[i]]] = 0.0
        P_hat[yis[yi[i]], xis[xi[i]]] = 1.0
    # Stop when error converges
    err = la.norm(np.dot(A, x_hat) - np.dot(P_hat.T, y))
    if err - prev_err < tol and err - prev_err > -tol:
        break

print x_hat
print x_true
print x_0
print sorted(yis.values())
