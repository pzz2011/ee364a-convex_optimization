from multi_risk_portfolio_data import *
import numpy as np
import cvxpy as cp

w = cp.Variable(n)
wc_risk = cp.Variable()

obj = cp.Maximize(mu.T * w - gamma * wc_risk)
cons = [cp.sum_entries(w) == 1]
cons += [cp.quad_form(w, Sigma_1) <= wc_risk]
cons += [cp.quad_form(w, Sigma_2) <= wc_risk]
cons += [cp.quad_form(w, Sigma_3) <= wc_risk]
cons += [cp.quad_form(w, Sigma_4) <= wc_risk]
cons += [cp.quad_form(w, Sigma_5) <= wc_risk]
cons += [cp.quad_form(w, Sigma_6) <= wc_risk]
prob = cp.Problem(obj, cons)

prob.solve()

# weights
print "Optimal weights:"
print w.value

# gamma_k are dual variables of the constraints
print "gamma_1:", cons[1].dual_variable.value
print "gamma_2:", cons[2].dual_variable.value
print "gamma_3:", cons[3].dual_variable.value
print "gamma_4:", cons[4].dual_variable.value
print "gamma_5:", cons[5].dual_variable.value
print "gamma_6:", cons[6].dual_variable.value

# the worst-case risk
print "Worst case risk:", wc_risk.value
