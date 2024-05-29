import math

def log_q(q, x):
    if q == 0:
        return math.log(x)
    else:
        return (x**q - 1)/q


