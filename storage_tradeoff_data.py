import numpy as np
import matplotlib.pyplot as plt
from cvxpy import *

np.random.seed(1)

T = 96
t = np.linspace(1, T, num=T).reshape(T,1)
p = np.exp(-np.cos((t-15)*2*np.pi/T)+0.01*np.random.randn(T,1))
u = 2*np.exp(-0.6*np.cos((t+40)*np.pi/T) - 0.7*np.cos(t*4*np.pi/T)+0.01*np.random.randn(T,1))

C = 3
D = 3
Q = 35
q = Variable(T)
c = Variable(T)
constraints = [c <= C, -c <= D, q <= Q, u + c >= 0, q[0] == q[T - 1] + c[T - 1], q >= 0]
for i in xrange(T - 1):
    constraints.append(q[i + 1] == q[i] + c[i])
obj = Minimize(p.T * (c + u))
prob = Problem(obj, constraints)
prob.solve()

plt.figure(1)
pline, = plt.plot(t, p);
uline, = plt.plot(t, u, 'r')
qline, = plt.plot(t, q.value, 'g')
cline, = plt.plot(t, c.value, 'y')
plt.legend([pline, uline, qline, cline], ['pt', 'ut', 'qt', 'ct'], loc = 1)
plt.show()

# Trade-off curves.
C = 3
D = 3
Q = Parameter(sign = 'positive')
q = Variable(T)
c = Variable(T)
constraints1 = [c <= C, -c <= D, q <= Q, u + c >= 0, q[0] == q[T - 1] + c[T - 1], q >= 0]
for i in xrange(T - 1):
    constraints1.append(q[i + 1] == q[i] + c[i])
obj1 = Minimize(p.T * (c + u))
prob1 = Problem(obj1, constraints1)
optimal1 = []
qvalues1 = np.linspace(1, 200, num = 400)
for val in qvalues1:
    Q.value = val
    prob1.solve()
    optimal1.append(prob1.value)

C = 1
D = 1
Q = Parameter(sign = 'positive')
q = Variable(T)
c = Variable(T)
constraints2 = [c <= C, -c <= D, q <= Q, u + c >= 0, q[0] == q[T - 1] + c[T - 1], q >= 0]
for i in xrange(T - 1):
    constraints2.append(q[i + 1] == q[i] + c[i])
obj2 = Minimize(p.T * (c + u))
prob2 = Problem(obj2, constraints2)
optimal2 = []
qvalues2 = np.linspace(1, 200, num = 400)
for val in qvalues2:
    Q.value = val
    prob2.solve()
    optimal2.append(prob2.value)

plt.figure(2)
q1, = plt.plot(qvalues1, optimal1)
q2, = plt.plot(qvalues2, optimal2)
plt.legend([q1, q2], ['C = D = 3', 'C = D = 1'])
plt.show()
