import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from cvxpy import *

h = 1.
g = 0.1
m = 10.
Fmax = 10.
p0 = np.matrix('50 ;50; 100')
v0 = np.matrix('-10; 0; -10')
alpha = 0.5
gamma = 1.
K = 35

#part (a)
e3 = np.row_stack((np.asmatrix(np.zeros((K))), np.asmatrix(np.zeros((K))), np.asmatrix(np.ones((K)))))
f = Variable(3, K)
p = Variable(3, K + 1)
v = Variable(3, K + 1)
sum_norm_f = 0
for i in xrange(K):
    sum_norm_f += norm(f[:, i])
obj = Minimize(gamma * h * sum_norm_f)
cons = [p[:, 0] == p0, v[:, 0] == v0, p[:, K] == 0, v[:, K] == 0,
v[:, 1:K+1] - v[:, 0:K] == (h/m) * f[:, 0:K] - h*g*e3,
p[:, 1:K+1] - p[:, 0:K] == h * 0.5 * (v[:, 1:K + 1] + v[:, 0:K])]
for i in xrange(K):
    cons.append(norm(f[:, i]) <= Fmax)
    cons.append(p[2, i] >= alpha * norm(p[0:2, i]))
cons.append(p[2, K] >= alpha * norm(p[0:2, K]))
prob = Problem(obj, cons)
prob.solve()
print "Minimum fuel consumption:", prob.value
# use the following code to plot your trajectories
# and the glide cone (don't modify)
# -------------------------------------------------------
fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.linspace(-40, 55, num=30)
Y = np.linspace(0, 55, num=30)
X, Y = np.meshgrid(X, Y)
Z = alpha*np.sqrt(X**2+Y**2)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
#Have your solution be stored in p
ax.plot(xs=p.value[0,:].A1,ys=p.value[1,:].A1,zs=p.value[2,:].A1)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
plt.show()

#part (b)
while(prob.status != 'infeasible'):
    K = K - 1
    p_opt = p.value
    v_opt = v.value
    e3 = np.row_stack((np.asmatrix(np.zeros((K))), np.asmatrix(np.zeros((K))), np.asmatrix(np.ones((K)))))
    f = Variable(3, K)
    p = Variable(3, K + 1)
    v = Variable(3, K + 1)
    sum_norm_f = 0
    for i in xrange(K):
        sum_norm_f += norm(f[:, i])
    obj = Minimize(gamma * h * sum_norm_f)
    cons = [p[:, 0] == p0, v[:, 0] == v0, p[:, K] == 0, v[:, K] == 0,
    v[:, 1:K+1] - v[:, 0:K] == (h/m) * f[:, 0:K] - h*g*e3,
    p[:, 1:K+1] - p[:, 0:K] == h * 0.5 * (v[:, 1:K + 1] + v[:, 0:K])]
    for i in xrange(K):
        cons.append(norm(f[:, i]) <= Fmax)
        cons.append(p[2, i] >= alpha * norm(p[0:2, i]))
    cons.append(p[2, K] >= alpha * norm(p[0:2, K]))
    prob = Problem(obj, cons)
    prob.solve()

print "Optimal K:", K+1
fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.linspace(-40, 55, num=30)
Y = np.linspace(0, 55, num=30)
X, Y = np.meshgrid(X, Y)
Z = alpha*np.sqrt(X**2+Y**2)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
#Have your solution be stored in p
ax.plot(xs=p_opt[0,:].A1,ys=p_opt[1,:].A1,zs=p_opt[2,:].A1)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
plt.show()
