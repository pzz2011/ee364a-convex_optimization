import numpy as np
import cvxpy as cp

a = np.array([0.2, 0.02, 0.04, 0.1])
A = np.diag(a)
b = np.array([0.5, 0.1, 0.0, 0.2])
b = np.asmatrix(b).T
p = cp.Variable(4)
obj = cp.Maximize(cp.geo_mean(p) - (0.5 * cp.quad_form(p, A) + b.T * p))
cons = [p > 0]
prob = cp.Problem(obj, cons)
prob.solve()

p_opt = p.value
print "Market clearing prices:"
print p_opt

print "Demand:"
print 0.25 * pow(p_opt[1, 0] * p_opt[2, 0] * p_opt[3, 0], 0.25) * pow(p_opt[0, 0], -3.0/4.0)
print 0.25 * pow(p_opt[0, 0] * p_opt[2, 0] * p_opt[3, 0], 0.25) * pow(p_opt[1, 0], -3.0/4.0)
print 0.25 * pow(p_opt[1, 0] * p_opt[0, 0] * p_opt[3, 0], 0.25) * pow(p_opt[2, 0], -3.0/4.0)
print 0.25 * pow(p_opt[1, 0] * p_opt[2, 0] * p_opt[0, 0], 0.25) * pow(p_opt[3, 0], -3.0/4.0)

print "Supply:"
print 0.2 * p_opt[0, 0] + 0.5
print 0.02 * p_opt[1, 0] + 0.1
print 0.04 * p_opt[2, 0]
print 0.1 * p_opt[3, 0] + 0.2
