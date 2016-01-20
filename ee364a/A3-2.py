from cvxpy import *

x = Variable()
y = Variable()

constraints = [x >= 0, y >= 0, 2*x + y >= 1, x + 3*y >= 1]
constraints1 = [x >= 0, y >= 0, 2*x + y >= 1, x + 3*y >= 1, x >= y]
constraints2 = [x >= 0, y >= 0, 2*x + y >= 1, x + 3*y >= 1, x <= y]

obj_a = Minimize(x + y)
obj_b = Minimize(- x - y)
obj_c = Minimize(x)
obj_d = Minimize(y)
obj_e = Minimize(x ** 2 + 9 * y ** 2)

prob_a = Problem(obj_a, constraints)
prob_a.solve()
print "(a)"
print "Status: a", prob_a.status
print "Optimal value ", prob_a.value
print "Optimal var", x.value, y.value

prob_b = Problem(obj_b, constraints)
prob_b.solve()
print "(b)"
print "Status: b", prob_b.status
print "Optimal value ", prob_b.value
print "Optimal var", x.value, y.value

prob_c = Problem(obj_c, constraints)
prob_c.solve()
print "(c)"
print "Status: c", prob_c.status
print "Optimal value ", prob_c.value
print "Optimal var", x.value, y.value

prob_d1 = Problem(obj_c, constraints1)
prob_d2 = Problem(obj_d, constraints2)
prob_d1.solve()
prob_d2.solve()
if(prob_d1.value >= prob_d2.value):
    print "(d)"
    print "Status: d", prob_d2.status
    print "Optimal value ", prob_d2.value
    print "Optimal var", x.value, y.value
else:
    prob_d1.solve()
    print "(d)"
    print "Status: d", prob_1.status
    print "Optimal value ", prob_d1.value
    print "Optimal var", x.value, y.value

prob_e = Problem(obj_e, constraints)
prob_e.solve()
print "(e)"
print "Status: e", prob_e.status
print "Optimal value ", prob_e.value
print "Optimal var", x.value, y.value
