import numpy as np
from math import *
n = 10 # number of variables
k = 6  # number of designs

# component widths from known designs
# each column of W is a different design
W ='1.8381    1.5803   12.4483    4.4542    6.5637    5.8225;\
    1.0196    3.0467   18.4965    3.6186    7.6979    2.3292;\
    1.6813    1.9083   17.3244    4.6770    4.6581   27.0291;\
    1.3795    2.6250   14.6737    4.1361    7.1610    7.5759;\
    1.8318    1.4526   17.2696    3.7408    2.2107   10.3642;\
    1.5028    3.0937   14.9034    4.4055    7.8582   20.5204;\
    1.7095    2.1351   10.1296    4.0931    2.9001    9.9634;\
    1.4289    3.5800    9.3459    3.8898    2.7663   15.1383;\
    1.3046    3.5610   10.1179    4.3891    7.1302    3.8139;\
    1.1897    2.7807   13.0112    4.2426    6.1611   29.6734'
W = np.matrix(W)

(W_min, W_max) = (1.0, 30.0)

# objective values for the different designs
# entry j gives the objective for design j
P = np.matrix('29.0148   46.3369  282.1749   78.5183  104.8087  253.5439')
D = np.matrix('15.9522   11.5012    4.8148    8.5697    8.0870    6.0273')
A = np.matrix('22.3796   38.7908  204.1574   62.5563   81.2272  200.5119')

# specifications
(P_spec, D_spec, A_spec) = (60.0, 10.0, 50.0)

print 'Possible W Design(i, j theta_lower, theta_upper):'
for i in xrange(6):
    for j in xrange(i+1, 6):
        if i != j:
            utheta = 1
            ltheta = 0
            tp = log(P_spec/P[0, j])/log(P[0, i]/P[0, j])
            if P[0, i] > P[0, j]:
                if tp < utheta:
                    utheta = tp
            else:
                if tp > ltheta:
                    ltheta = tp
            td = log(D_spec/D[0, j])/log(D[0, i]/D[0, j])
            if D[0, i] > D[0, j]:
                if td < utheta:
                    utheta = td
            else:
                if td > ltheta:
                    ltheta = td
            ta = log(A_spec/A[0, j])/log(A[0, i]/A[0, j])
            if A[0, i] > A[0, j]:
                if ta < utheta:
                    utheta = ta
            else:
                if ta > ltheta:
                    ltheta = ta
            if utheta > ltheta:
                print i, j, ltheta, utheta

print '\nOne Example:'
print 'W:'
for i in xrange(10):
    print W[i, 0]**0.52 * W[i, 3]**0.48

print 'P:', P[0, 1]**0.52 * P[0, 3]**0.48
print 'D:', D[0, 1]**0.52 * D[0, 3]**0.48
print 'A:', A[0, 1]**0.52 * A[0, 3]**0.48
