import numpy as np
from cvxpy import *

(m, n) = (30, 10)
A = np.random.rand(m, n); A = np.asmatrix(A)
b = np.random.rand(m, 1); b = np.asmatrix(b)
c_nom = np.ones((n, 1)) + np.random.rand(n, 1); c_nom = np.asmatrix(c_nom)

Iplus = np.eye(n)
onetn = np.ones((1, n)) / n;
F = np.array(list(Iplus) + list(-Iplus) + list(onetn) + list(-onetn))
g = np.array(list(1.25 * c_nom) + list(0.75 * c_nom))
g = np.append(g, [[np.sum(c_nom) * 1.1 / n]])
g = np.append(g, [[np.sum(c_nom) * 0.9 / n]])

lam = Variable(2 * n + 2)
obj1 = Minimize(g.T * lam)
cons1 = [lam >= 0, A * F.T * lam >= b]
prob1 = Problem(obj1, cons1)
prob1.solve()
print "Worst-case cost:", prob1.value
x_ = np.dot(F.T, lam.value)
wc_nom = np.dot(c_nom.T, x_)
print "Worst-case nominal cost:", wc_nom[0, 0]

x = Variable(n)
obj2 = Minimize(c_nom.T * x)
cons2 = [A * x >= b]
prob2 = Problem(obj2, cons2)
prob2.solve()
print "Nominal cost:", prob2.value
