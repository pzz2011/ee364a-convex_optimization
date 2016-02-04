import numpy as np
from cvxpy import *
import matplotlib.pyplot as plt

np.random.seed(0)
(m, n) = (300, 100)
A = np.random.rand(m, n); A = np.asmatrix(A)
b = A.dot(np.ones((n, 1)))/2; b = np.asmatrix(b)
c = -np.random.rand(n, 1); c = np.asmatrix(c)

x = Variable(n)
constraints = [A * x <= b, x >= 0, x <= 1]
obj = Minimize(c.T * x)
prob = Problem(obj, constraints)
prob.solve()

lower = prob.value
xrlx = x.value
xrlx.squeeze()

thresholds = np.arange(0, 1.01, 0.01)
tnum = len(thresholds)
objectives = []
violations = []

for t in thresholds:
    xnew = np.random.rand(n, 1)
    xnew = np.asmatrix(xnew)
    for i in xrange(n):
        if xrlx[i] >= t:
            xnew[i, 0] = 1
        else:
            xnew[i, 0] = 0

    objectives.append(np.dot(c.T, xnew)[0, 0])
    vio = np.dot(A, xnew) - b
    violations.append(np.amax(vio))

c = 0
for i in xrange(100):
    if violations[i] < 0:
        c = i
        break

plt.plot(thresholds[0 : c + 1], violations[0 : c + 1], linewidth = 2)
plt.plot(thresholds[c + 1 : tnum], violations[c + 1 : tnum], linewidth = 2)
plt.plot(thresholds, [0]*101, linewidth = 3, color = 'black')
plt.xlabel('threshold')
plt.ylabel('max violation')
plt.show()

plt.plot(thresholds[0 : c + 1], objectives[0 : c + 1], linewidth = 2)
plt.plot(thresholds[c + 1 : tnum], objectives[c + 1 : tnum], linewidth = 2)
plt.plot(thresholds, [objectives[c]]*101, linewidth = 3, color = 'black')
plt.xlabel('threshold')
plt.ylabel('objective')
plt.show()

print 'L = ', lower
print 'U = ', objectives[c]
print 't = ', thresholds[c]
