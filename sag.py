from qgasdev import qgasdev
from qexp import exp_q  
from qlog import log_q
from sir_MultiPop import func

import random
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


"""Definição dos parâmetros da simulação"""
tmax = 400 #numero maximo de iterações
rest = 20 #restart
qa = 0.0 #parametro de generalização da aceitação
qv = 0.7 #parametro de generalização da visitação
alfa = 0.9 #taxa de resfriamento da temperatura de de aceitação
p0 = 0.9 #probabilidade de definir a temperatura inicial de aceitação
nd = 10 #dimensão do vetor solução
xmin = 0.0 #limite inferior do espaço de solução
xmax = 1.0 #limite superior do espaço de solução
f_old = 0.0 #funcional gerado pela solução antiga
f_new = 0.0 #funcional gerado pela nova solução
f_min = 0.0 #minimo funcional de erro (random_walk inicial)
f_max = 0.0 #maximo funcional de erro (random_walk inicial)
amp_f = 0.0 #amplitude do funcional de erro (random_walk inicial)

"""Listas para armazenar os resultados da simulação"""
Ta_res = []
Tv_res = []
x_res = []
f_res = []

"""Definição da temperatura inicial de visitação"""
Tv0 = (xmax - xmin)
Tv = Tv0 

x_old = np.zeros(nd)

"""Determinação de uma temperatura inicial"""
for w in range(nd):
    x_old[w] = xmin + (xmax - xmin)*random.random()
x_old = x_old/np.sum(x_old) #para percentualizar e a soma de todos se manter um

'''Cálculo da função objetivo inicial'''
f_old = func(x_old)

'''Atribuição inicial para os valores f_min e f_max'''
f_max = 1.1*f_old
f_min = 0.9*f_old

for i in range(100): #inicio do random_walk
    '''Geração de uma nova solução'''
    for w in range(nd):
        x_old[w] = xmin + (xmax - xmin)*random.random()
    x_old = x_old/np.sum(x_old) #para percentualizar e a soma de todos se manter um

    '''Cálculo da nova função objetivo'''
    f_old = func(x_old)

    '''Funcional para procurar o valor mínimo f_min da função objetivo'''
    if f_old < f_min:
        f_min = f_old

    '''Condicional para procurar o valor máximo f_max da função objetivo'''
    if f_old > f_max:
        f_max = f_old

    '''Cálculo da amplitude da função objetivo'''
    amp_f = f_max - f_min

'''Determinação da temperatura inicial'''
Ta0 = -(amp_f/log_q(qa, p0))
Ta = Ta0

"""Definição da solução inicial e inicialização dos vetores x_aux e x_new"""
for w in range(nd):
    x_old[w] = xmin + (xmax - xmin)*random.random()
x_old = x_old/np.sum(x_old)

#Se eu colocar apenas x_aux = x_old eles vão apontar pro mesmo endereço e a mudança em um também acontecerá no outro
x_aux = np.array(x_old)
x_new = np.array(x_old)

f_old = func(x_old)

'''Salvando os valores encontrados'''
Ta_res += [Ta]
Tv_res += [Tv]
x_res.append(x_old.copy())
f_res += [f_old]

"""Inicio do loop do simulated anneling"""
for t in range(tmax):
    '''Inicio do restart'''
    for k in range(rest):
        '''Inicio da avaliação do elemento 'w' da solução'''
        for w in range(nd):
            '''Geração do novo vetor solução'''
            x_new[w] = 1.1*xmax #forçando a entrada no whike
            while x_new[w] < xmin or x_new[w] > xmax:
                x_new[w] = x_old[w] + Tv*qgasdev(qv)

        x_new = x_new/np.sum(x_new) #normalização da solução gerada

        '''Determinação do novo valor da função objetivo'''
        f_new = func(x_new)

        '''Crieterio de Metropolis'''
        if f_new < f_old:
            for i in range(nd):
                x_aux[i] = x_new[i]
        else:
            pa = random.random() #Probabilidade aleatória
            paceite = exp_q(qa, (f_old-f_new)/Ta)

            if paceite > pa:
                for i in range(nd):
                    x_aux[i] = x_new[i]
    
        '''Atualização do vetor solução e da função objetivo'''
        for i in range(nd):
            x_old[i] = x_aux[i]
        f_old = func(x_old)

    '''Resfriamento da temperatura de visitação'''
    Tv = Tv0*log_q(qv, 2)/log_q(qv, 1 + t+1) #No matlab esse t começa em 1
    
    '''Resfriamento da temperatura de aceitação'''
    Ta = Ta0*alfa**t

    '''Salvando os valores encontrados'''
    Ta_res += [Ta]
    Tv_res += [Tv]
    x_res.append(x_old.copy())
    f_res += [f_old]

"""Armazenamento dos valores"""
df = pd.DataFrame({
    'Temperatura de aceitação': Ta_res,
    'Temperatura de visitação': Tv_res,
    'Vetor solução': x_res,
    'Valor da função': f_res
})
df.to_csv("./resultados_SIR.csv", sep=',')


"""Geração do gráfico"""
'''Valores para a plotagem'''
f = f_res
iterations = np.arange(1, len(f) + 1)

rho_data = np.array(x_res)
t_iter = np.arange(1, tmax + 2)

'''Criação da figura com 2 sublots'''
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
fig.suptitle('Resultados do Annealing')

'''Gráfico da função objetivo'''
ax1.plot(iterations, f, 'r')
ax1.set_xlim([0, len(f)])
ax1.set_ylim([min(f), max(f)])
ax1.set_xlabel('Iteração', fontsize=12)
ax1.set_ylabel('Número de Infectados', fontsize=12)
#ax1.legend(loc="upper right")

'''Gráfico dos valores de rho'''
for i in range(nd):
    colors = np.random.rand(3)
    ax2.plot(rho_data[:,i], t_iter, color=colors, label=f'$\\rho_{(i + 1)}$')
ax2.set_xlim([0, 1])
ax2.set_ylim([0, tmax])
ax2.set_xlabel(r'$\rho$', fontsize=12)
ax2.set_ylabel('Iteração', fontsize=12)
ax2.invert_yaxis()
ax2.legend(loc="upper right")

'''Mostrando o gráfico'''
plt.show()







from qgasdev import qgasdev
from qexp import exp_q  
from qlog import log_q
from sir_MultiPop import func

import random
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


"""Definição dos parâmetros da simulação"""
tmax = 100 #numero maximo de iterações
rest = 10 #restart
qa = 0.0 #parametro de generalização da aceitação
qv = 0.7 #parametro de generalização da visitação
alfa = 0.9 #taxa de resfriamento da temperatura de de aceitação
p0 = 0.9 #probabilidade de definir a temperatura inicial de aceitação
nd = 3 #dimensão do vetor solução
xmin = 0.0 #limite inferior do espaço de solução
xmax = 1.0 #limite superior do espaço de solução
f_old = 0.0 #funcional gerado pela solução antiga
f_new = 0.0 #funcional gerado pela nova solução
f_min = 0.0 #minimo funcional de erro (random_walk inicial)
f_max = 0.0 #maximo funcional de erro (random_walk inicial)
amp_f = 0.0 #amplitude do funcional de erro (random_walk inicial)

"""Listas para armazenar os resultados da simulação"""
Ta_res = []
Tv_res = []
x_res = []
f_res = []

"""Definição da temperatura inicial de visitação"""
Tv0 = (xmax - xmin)
Tv = Tv0 

x_old = np.zeros(nd)

"""Determinação de uma temperatura inicial"""
for w in range(nd):
    x_old[w] = xmin + (xmax - xmin)*random.random()
x_old = x_old/np.sum(x_old) #para percentualizar e a soma de todos se manter um

'''Cálculo da função objetivo inicial'''
f_old = func(x_old)

'''Atribuição inicial para os valores f_min e f_max'''
f_max = 1.1*f_old
f_min = 0.9*f_old

for i in range(100): #inicio do random_walk
    '''Geração de uma nova solução'''
    for w in range(nd):
        x_old[w] = xmin + (xmax - xmin)*random.random()
    x_old = x_old/np.sum(x_old) #para percentualizar e a soma de todos se manter um

    '''Cálculo da nova função objetivo'''
    f_old = func(x_old)

    '''Funcional para procurar o valor mínimo f_min da função objetivo'''
    if f_old < f_min:
        f_min = f_old

    '''Condicional para procurar o valor máximo f_max da função objetivo'''
    if f_old > f_max:
        f_max = f_old

    '''Cálculo da amplitude da função objetivo'''
    amp_f = f_max - f_min

'''Determinação da temperatura inicial'''
Ta0 = -(amp_f/log_q(qa, p0))
Ta = Ta0

"""Definição da solução inicial e inicialização dos vetores x_aux e x_new"""
for w in range(nd):
    x_old[w] = xmin + (xmax - xmin)*random.random()
x_old = x_old/np.sum(x_old)

#Se eu colocar apenas x_aux = x_old eles vão apontar pro mesmo endereço e a mudança em um também acontecerá no outro
x_aux = np.array(x_old)
x_new = np.array(x_old)

f_old = func(x_old)

'''Salvando os valores encontrados'''
Ta_res += [Ta]
Tv_res += [Tv]
x_res.append(x_old.copy())
f_res += [f_old]

"""Inicio do loop do simulated anneling"""
for t in range(tmax):
    '''Inicio do restart'''
    for k in range(rest):
        '''Inicio da avaliação do elemento 'w' da solução'''
        for w in range(nd):
            '''Geração do novo vetor solução'''
            x_new[w] = 1.1*xmax #forçando a entrada no whike
            while x_new[w] < xmin or x_new[w] > xmax:
                x_new[w] = x_old[w] + Tv*qgasdev(qv)

        x_new = x_new/np.sum(x_new) #normalização da solução gerada

        '''Determinação do novo valor da função objetivo'''
        f_new = func(x_new)

        '''Crieterio de Metropolis'''
        if f_new < f_old:
            for i in range(nd):
                x_aux[i] = x_new[i]
        else:
            pa = random.random() #Probabilidade aleatória
            paceite = exp_q(qa, (f_old-f_new)/Ta)

            if paceite > pa:
                for i in range(nd):
                    x_aux[i] = x_new[i]
    
        '''Atualização do vetor solução e da função objetivo'''
        for i in range(nd):
            x_old[i] = x_aux[i]
        f_old = func(x_old)

    '''Resfriamento da temperatura de visitação'''
    Tv = Tv0*log_q(qv, 2)/log_q(qv, 1 + t+1) #No matlab esse t começa em 1
    
    '''Resfriamento da temperatura de aceitação'''
    Ta = Ta0*alfa**t

    '''Salvando os valores encontrados'''
    Ta_res += [Ta]
    Tv_res += [Tv]
    x_res.append(x_old.copy())
    f_res += [f_old]

"""Armazenamento dos valores"""
df = pd.DataFrame({
    'Temperatura de aceitação': Ta_res,
    'Temperatura de visitação': Tv_res,
    'Vetor solução': x_res,
    'Valor da função': f_res
})
df.to_csv("./resultados_SIR.csv", sep=',')


"""Geração do gráfico"""
'''Valores para a plotagem'''
f = f_res
iterations = np.arange(1, len(f) + 1)

rho_data = np.array(x_res)
t_iter = np.arange(1, tmax + 2)

'''Criação da figura com 2 sublots'''
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
fig.suptitle('Resultados do Annealing')

'''Gráfico da função objetivo'''
ax1.plot(iterations, f, 'r')
ax1.set_xlim([0, len(f)])
ax1.set_ylim([min(f), max(f)])
ax1.set_xlabel('Iteração', fontsize=12)
ax1.set_ylabel('Número de Infectados', fontsize=12)
#ax1.legend(loc="upper right")

'''Gráfico dos valores de rho'''
for i in range(nd):
    colors = np.random.rand(3)
    ax2.plot(rho_data[:,i], t_iter, color=colors, label=f'$\\rho_{(i + 1)}$')
ax2.set_xlim([0, 1])
ax2.set_ylim([0, tmax])
ax2.set_xlabel(r'$\rho$', fontsize=12)
ax2.set_ylabel('Iteração', fontsize=12)
ax2.invert_yaxis()
ax2.legend(loc="upper right")

'''Mostrando o gráfico'''
plt.show()











