import numpy as np
import numpy.linalg as la
from cvxpy import *

(m, n) = (4, 3)
A_bar = np.array([[60., 45., -8.], [90., 30., -30.], [0., -8., -4.], [30., 10., -10.]])
R = 0.05 * np.ones((4, 3))
b = np.array([[-6.], [-3.], [18.], [-9.]])

# Robust least squares
x = Variable(n)
y = Variable(m)
obj1 = Minimize(norm(y))
cons1 = []
for i in xrange(m):
    cons1.append(A_bar[i, :] * x - b[i] + R[i, :] * abs(x) <= y[i])
    cons1.append(-A_bar[i, :] * x + b[i] + R[i, :] * abs(x) <= y[i])

prob1 = Problem(obj1, cons1)
prob1.solve()
x_rls = x.value
rls_wc_norm = prob1.value
rls_nominal_norm = la.norm(np.dot(A_bar, x_rls) - b, 2)

# Least squares
x = Variable(n)
obj2 = Minimize(norm(A_bar * x - b))
cons2 = []
prob2 = Problem(obj2, cons2)
prob2.solve()
x_ls = x.value
ls_nominal_norm = prob2.value

# Worst case norm for x_ls
y = Variable(m)
obj3 = Minimize(norm(y))
cons3 = []
for i in xrange(m):
    cons3.append(A_bar[i, :] * x - b[i] + R[i, :] * abs(x_ls) <= y[i])
    cons3.append(-A_bar[i, :] * x + b[i] + R[i, :] * abs(x_ls) <= y[i])

prob3 = Problem(obj3, cons3)
prob3.solve()
ls_wc_norm = prob3.value

print "Least square x:", x_ls
print "Robust least square x:", x_rls
print "Nominal residual value of least square x:", ls_nominal_norm
print "Nominal residual value of robust least square x:", rls_nominal_norm
print "Worst case residual value of least square x:", ls_wc_norm
print "Worst case residual value of robust least square x:", rls_wc_norm
