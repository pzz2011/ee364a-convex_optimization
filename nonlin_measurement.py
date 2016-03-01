import numpy as np
from nonlin_meas_data import *
from cvxpy import *
import matplotlib.pyplot as plt

x = Variable(n)
z = Variable(m)

obj = Minimize(norm(z - A * x))
cons = []
for i in xrange(m - 1):
    cons.append(1.0/beta * (y[i+1] - y[i]) <= z[i+1] - z[i])
    cons.append(1.0/alpha * (y[i+1] - y[i]) >= z[i+1] - z[i])
prob = Problem(obj, cons)
prob.solve()

xopt = x.value
zopt = z.value

print xopt

plt.plot(zopt, y)
plt.xlabel('$\hat{z}$')
plt.ylabel('$y = \hat{\Phi}(z)$')
plt.show()
