import numpy as np
import numpy.linalg as la
import time

n = 2500;
k = 30;

mu = np.random.rand(n, 1) * 2 - 1
D = np.diag(np.random.rand(n) + np.ones(n))
Q = np.random.rand(k, k)
Q = np.dot(Q.T, Q) + np.eye(k)
F = np.random.rand(n, k) * 2 - 1
one_n = np.ones((n, 1))
zero_k = np.zeros((k, 1))

t1_start = time.time()
Sigma = np.dot(np.dot(F, Q), F.T) + D
L = la.cholesky(Sigma)
nu = (np.dot(one_n.T, la.solve(L.T, la.solve(L, mu))) - 1) / np.dot(one_n.T, la.solve(L.T, la.solve(L, one_n)))
w_a = la.solve(L.T, la.solve(L, mu - nu * one_n))

print "Time for part (a):", time.time() - t1_start

t2_start = time.time()

G = np.vstack((np.hstack((one_n, F)), np.hstack((zero_k, -np.eye(k)))))
D_inv = 1/np.diag(D)
L = la.cholesky(Q)
H_inv_G = np.vstack((np.multiply(np.repeat(np.asmatrix(D_inv).T, k+1, axis = 1), G[0:n, :]), la.solve(L.T, la.solve(L, G[n:, :]))))
H_inv_mu = np.vstack((np.multiply(np.asmatrix(D_inv).T , mu), zero_k))
g = la.solve(np.dot(G.T, H_inv_G), np.dot(G.T, H_inv_mu) - np.vstack((1, zero_k)))
w_b = np.multiply((np.asmatrix(D_inv).T)[:, 0], (mu - np.dot(G[0:n, :], g))[:, 0])

print "Time for part (b):", time.time() - t2_start
