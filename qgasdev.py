import math
import random

def qgasdev(q):
    #Cálculo do qaux para geração da distribuição q-Gaussiana
    qaux = (1+(q+1))/(3-(q+1))

    #Geração de dois números aleatórios no intervalo de 0-1
    u1 = random.random()
    u2 = random.random()

    qlog = 0

    if qaux == 1:
        qlog = math.log(u1)
    else:
        qlog = (u1**(1-qaux) - 1)/(1 - qaux)

    return math.sqrt(-2*qlog)*math.sin(2*math.pi*u2)
