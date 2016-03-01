import numpy as np
import matplotlib.pyplot as plt
from cvxpy import *

k = 201
t = np.linspace(-3, 3, num = k, endpoint = True)
y = np.exp(t)

# Using bisection to find the desired u
low = 0.0
up = 1.0
tol = 0.001
while(up - low > tol):
    u = (up + low)/2
    a = Variable(3)
    b = Variable(2)
    obj = Minimize(0)
    cons = []
    for i in xrange(k):
        cons.append(abs((a[0] + a[1] * t[i] + a[2] * t[i] ** 2) - y[i] * (1 + b[0] * t[i] + b[1] * t[i] ** 2)) <= u * (1 + b[0] * t[i] + b[1] * t[i] ** 2))
    prob = Problem(obj, cons)
    prob.solve()
    if(prob.status == "infeasible"):
        low = u
    else:
        up = u
        a_opt = a.value
        b_opt = b.value
        u_opt = u

print u
print a_opt
print b_opt

y_pred = np.zeros(k)
for i in xrange(k):
    y_pred[i] = (a_opt[0] + a_opt[1] * t[i] + a_opt[2] * t[i] ** 2)/(1 + b_opt[0] * t[i] + b_opt[1] * t[i] ** 2)

plt.plot(t, y)
plt.scatter(t, y_pred, color = 'red', marker = "x")
plt.xlabel('$t$')
plt.ylabel('$y$')
plt.show()

y_residual = y_pred - y
plt.plot(t, y_residual, color = 'purple', linewidth = 1.5)
plt.xlabel('$t_i$')
plt.ylabel('$f(t_i) - y_i$')
plt.show()
