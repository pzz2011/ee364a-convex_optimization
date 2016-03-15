import numpy as np
import numpy.linalg as la
import cvxpy as cp
import matplotlib.pyplot as plt

def newton(A, b, c, x_0):
    #algorithm parameters
    alpha = 0.1
    beta = 0.5
    epsilon = 1e-5
    max_iters = 50

    m = b.size
    n = x_0.size

    #initialization
    nu = np.zeros(m)
    x = x_0
    residuals = []

    for i in xrange(max_iters):
        H = np.diag(pow(x, -2))
        r_dual = c - pow(x, -1) + np.dot(A.T, nu)
        r_pri = np.dot(A, x) - b
        r = np.append(r_dual, r_pri)

        #check for convergence
        r_norm = la.norm(r)
        residuals.append(r_norm)
        if r_norm <= epsilon and la.norm(np.dot(A, x) - b) <= epsilon:
            break

        #compute newton step via whole KKT system
        M = np.bmat([[H, A.T], [A, np.zeros((m, m))]])
        d = la.solve(M, -r)
        d_x = d[: n]
        d_nu = d[n :]

        #backtracking line search
        t = 1
        # first bring point into domain
        while np.min(x + t * d_x) <= 0:
            t = beta * t

        # now do backtracking line search
        r_dual_new = c - np.power(x + t * d_x, -1) + A.T.dot(nu + t * d_nu)
        r_pri_new = np.dot(A, x + t * d_x) - b
        while la.norm(np.append(r_dual_new, r_pri_new)) > (1 - alpha * t) * r_norm:
            t = beta * t;
            r_dual_new = c - pow(x + t * d_x, -1) + np.dot(A.T, nu + t * d_nu)
            r_pri_new = np.dot(A, x + t * d_x) - b

        # update primal and dual variables
        x = x + t* d_x
        nu = nu + t * d_nu

    if i == max_iters - 1:
        print "ERROR: max_iters reached."
        return (None, None, i)
    else:
        return (x, nu, i)

def barrier(A, b, c, mu):
    (m, n) = A.shape
    epsilon = 1e-3

    x = np.ones(n)
    t = 1.0
    (x_star, nu_star, k) = newton(A, b, t * c, x)
    x = x_star
    h = np.array([k, n/t])
    h = np.asmatrix(h).T
    history = h
    while 1:
        (x_star, nu_star, k) = newton(A, b, t * c, x)
        x = x_star
        h = np.array([k, n/t])
        h = np.asmatrix(h).T
        history = np.hstack((history, h))
        if n/t < epsilon:
            break
        t = mu * t

    nu_star = nu_star/t
    return x_star, nu_star, history

m = 100
n = 500
A = np.zeros((m, n))
while la.matrix_rank(A) < m:
    A = np.random.rand(m, n)
    A[0, :] = np.absolute(A[0, :])

p = np.absolute(np.random.rand(n))
b = np.dot(A, p)
c = np.random.rand(n)
(x_star, nu_star, history) = barrier(A, b, c, 10)
h0 = []
h1 = []
hcum = np.cumsum(history[0, :])
for i in xrange(history.shape[1]):
    h0.append(hcum[0, i])
    h1.append(history[1, i])
plt.step(h0, h1)
plt.yscale("log")
plt.show()

x = cp.Variable(n)
obj = cp.Minimize(c.T * x)
cons = [A * x == b, x >= 0]
prob = cp.Problem(obj, cons)
prob.solve()
print la.norm(x_star - x.value)
print la.norm(nu_star - cons[0].dual_value)

for mu in [2, 3, 5, 10, 20, 40, 100]:
    (x_star, nu_star, history) = barrier(A, b, c, mu)
    h0 = []
    h1 = []
    hcum = np.cumsum(history[0, :])
    for i in xrange(history.shape[1]):
        h0.append(hcum[0, i])
        h1.append(history[1, i])
    plt.step(h0, h1)
plt.yscale("log")
plt.xlabel("Newton iterations")
plt.ylabel("Duality gaps")
plt.show()
