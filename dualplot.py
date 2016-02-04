import numpy as np
from math import *
import matplotlib.pyplot as plt

xs = np.arange(-1, 5, 0.01)
lambdas = np.arange(0, 4, 0.5)

for l in lambdas:
    L = []
    for x in xs:
        L.append((1 + l)*x**2 - 6*l*x + 8*l + 1)
    plt.plot(xs, L)

plt.show()

ls = np.arange(-0.5, 5, 0.01)
g = []
for l in ls:
    g.append(-9*l**2/(1+l) + 1 + 8*l)

plt.plot(ls, g)
plt.show()

us = np.arange(-1, 10, 0.01)
p = []
for u in us:
    if u > 8:
        p.append(1)
    else:
        p.append(u - 6 * sqrt(1+u) + 11)

plt.plot(us, p)
plt.xlim([-2, 10])
plt.ylim([-2, 10])
plt.show()
