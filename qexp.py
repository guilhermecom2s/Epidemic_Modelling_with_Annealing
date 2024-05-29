import math

def exp_q(q, x):
    if q == 0:
        return math.exp(x)
    else:
        return (1+q*x)**(1/q)

