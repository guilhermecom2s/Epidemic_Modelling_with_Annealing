import numpy as np

from matplotlib import pyplot as plt
from scipy.integrate import odeint

def sis_equacoes(w, t, P):
    """
    Sistema de equações do modelo SIR
    """
    N, beta, gama = P #parâmetros para as equações
    S, I, R = w #valores de Suscetíves, Infectados e Recuperados

    dwdt = [-beta*S*I/N, beta*S*I/N - gama*I, gama*I] #sistema com as três equações do modelo SIR

    return dwdt

"""Parâmetros globais do modelo"""
N = 10**5 #tamanho da população
beta = 0.5 #coeficiente de transmissão (1/dia)
gama = 0.1 #inverso do período infeccioso (1/dia)

P = [N, beta, gama] #vetor para armazenamento dos parâmetros globais


"""Intervalos de tempo para a simulação"""
ti = 0; #tempo inicial (dias)
tf = 100; #tempo final (dias)
tspan = np.linspace(ti, tf, 5*(tf-ti)) #500 pontos (5*100) para saída de dados


"""Condições iniciais"""
I0 = 1.0 #número de indíviduos infectados inicialmente
S0 = N - I0 #número de indíviduos suscetíves inicialmente
R0 = 0.0 #número de indíviduio recuperados inicialmente

W0 = [S0, I0, R0] #vetor com as condições iniciais


"""Solução do modelo SIR"""
sol = odeint(sis_equacoes, W0, tspan, args= (P,)) #resolução do sistema de equações


"""Plotagem do gráfico"""
S = sol[:,0] #pegando o valor do primeiro elemento da lista do sistema de equações
I = sol[:,1] #pegando o valor do segundo elemento da lista do sistema de equações
R = sol[:,2] #pegando o valor do terceiro elemento da lista do sistema de equações

plt.plot(tspan, S, 'r', label = 'Suscetíveis')
plt.plot(tspan, I, 'b', label = 'Infectados')
plt.plot(tspan, R, 'g', label = 'Recuperados') 
plt.xlabel('t(dias)')
plt.ylabel('Número de Indivíduos')
plt.legend()
#Descomentar as linhas abaixos para inserir uma caixa de texto com os parâmetros utilizados
#info_text = f'Beta: {beta}\nGama: {gama} '
#plt.text(0, 0, info_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
plt.show()
