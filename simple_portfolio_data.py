import numpy as np
from cvxpy import *
import math
import matplotlib.pyplot as plt

np.random.seed(1)
n = 20
pbar = np.ones((n,1))*.03 + np.r_[np.random.rand(n-1,1), np.zeros((1,1))]*.12;
S = np.random.randn(n, n); S = np.asmatrix(S)
S = S.T*S
S = S/max(np.abs(np.diag(S)))*.2
S[:, -1] = np.zeros((n, 1))
S[-1, :] = np.zeros((n, 1)).T
x_unif = np.ones((n, 1))/n; x_unit = np.asmatrix(x_unif)

# Uniform portfolio
print "[Uniform portfolio]"
print "Optimal standard deviation of risk: ", math.sqrt(np.dot(np.dot(x_unit.T, S), x_unit))

# Unconstrained portfolio
uni = np.ones((1, n))
x = Variable(n)
constraints = [uni * x == 1, pbar.T * x == pbar.T * x_unit]
obj = Minimize(quad_form(x, S))
prob = Problem(obj, constraints)
prob.solve()
risksdv = math.sqrt(prob.value)
print "[Unconstrained portfolio]"
print "Status: ", prob.status
print "Optimal standard deviation of risk: ", risksdv

# Long-only portfolio
uni = np.ones((1, n))
x = Variable(n)
constraints = [uni * x == 1, pbar.T * x == pbar.T * x_unit, x>= 0]
obj = Minimize(quad_form(x, S))
prob = Problem(obj, constraints)
prob.solve()
risksdv = math.sqrt(prob.value)
print "[Long-only portfolio]"
print "Status: ", prob.status
print "Optimal standard deviation of risk: ", risksdv

# Short-limited portfolio
uni = np.ones((1, n))
x = Variable(n)
constraints = [uni * x == 1, pbar.T * x == pbar.T * x_unit, uni * max_elemwise(-x, 0) <= 0.5]
obj = Minimize(quad_form(x, S))
prob = Problem(obj, constraints)
prob.solve()
risksdv = math.sqrt(prob.value)
print "[Unconstrained portfolio]"
print "Status: ", prob.status
print "Optimal standard deviation of risk: ", risksdv

# Trade-off curves.
lam = Parameter(sign = 'positive')
x = Variable(n)
constraints1 = [uni * x == 1, x >= 0]
constraints2 = [uni * x == 1, uni * max_elemwise(-x, 0) <= 0.5]
obj = Minimize(-pbar.T * x + lam * quad_form(x, S))
prob1 = Problem(obj, constraints1)
prob2 = Problem(obj, constraints2)
meanl = []
means = []
stdl = []
stds = []
lamvals = np.linspace(0, 50, num = 50)
for val in lamvals:
    lam.value = val
    prob1.solve()
    meanl.append(np.dot(pbar.T, x.value)[0, 0])
    stdl.append(math.sqrt(np.dot(np.dot(x.value.T, S), x.value)))
    prob2.solve()
    means.append(np.dot(pbar.T, x.value)[0, 0])
    stds.append(math.sqrt(np.dot(np.dot(x.value.T, S), x.value)))

plt.figure()
blue, = plt.plot(stdl, meanl, label = 'Long-only portfolio')
green, = plt.plot(stds, means, label = 'Limit on total short position')
plt.xlabel('Standard deviation')
plt.ylabel('Mean return')
plt.title('Standard deviation VS Mean return')
plt.legend([blue, green], ['Long-only portfolio', 'Limit on total short position'], loc = 4)
plt.show()
