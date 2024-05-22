"""Importação de Bibliotecas"""
import numpy as np
import pandas as pd

from scipy.integrate import odeint
from matplotlib import pyplot as plt

class population(object):
    """
    Classe que representa uma população
    """
    def __init__(self, N, mu, beta, gama, rho):
        ALPHA = 0.05 #taxa de vacinação de suscetíveis

        self.N = N #número de indivíduos na população
        self.mu = mu #taxa de mortalidadee natalidade da população
        self.beta = beta #vetor com os valores de beta 
        self.gama = gama #taxa de recuperação
        self.rho = rho #fração da vacinação
        #self.alpha = alpha #taxa de vacinação de S
        self.alpha = rho*ALPHA
     
    def condicoes_iniciais(self):
        """
        Retorna um vetor com as condições iniciais do problema
        """
        I0 = 1.0 #número de indíviduos infectados inicialmente
        S0 = self.N - I0 #número de indíviduos suscetíves inicialmente
        R0 = 0.0 #número de indíviduio recuperados inicialmente
        Icum0 = I0 #número inicial de infectados acumulados da população

        W0 = [S0, I0, R0, Icum0] #vetor com as condições iniciais

        return W0
    
def intervalo_tempo(ti, tf):
    """
    Retorna um vetor com os intervalos de tempo para a simulação
    """
    tspan = np.linspace(ti, tf, 5*(tf-ti)) #500 pontos (5*100) para saída de dados

    t = [ti, tf, tspan] #vetor com as informações relativas ao tempo

    return t

def gerar_equacoes(num_pops):
    """
    Retorna as equações para um número 'num_pops' de popualações
    """
    equacoes = []
    
    for i in range(num_pops):
        S = f"S{i+1}"
        I = f"I{i+1}"
        R = f"R{i+1}"
        
        beta_terms = ' + '.join([f"Pops[{i}].beta[{j}] * I{j+1}" for j in range(num_pops)])
        
        dS_dt = f"Pops[{i}].mu * Pops[{i}].N - ({S} * ({beta_terms}) / Pops[{i}].N) - Pops[{i}].alpha * {S} - Pops[{i}].mu * {S}"
        dI_dt = f"({S} * ({beta_terms}) / Pops[{i}].N) - Pops[{i}].gama * {I} - Pops[{i}].mu * {I}"
        dR_dt = f"Pops[{i}].gama * {I} + Pops[{i}].alpha * {S} - Pops[{i}].mu * {R}"
        Icum = f"{S} * ({beta_terms}) / Pops[{i}].N"
        
        equacoes.append(dS_dt)
        equacoes.append(dI_dt)
        equacoes.append(dR_dt)
        equacoes.append(Icum)
    
    return equacoes

def gerar_ode(num_pops):
    """
    Escreve uma função de ode's para ser executada pelo odeint
    """
    equacoes = gerar_equacoes(num_pops)
    
    func_ode = "def ode_system(y, t, Pops):\n"
    func_ode += "    dydt = []\n"
    
    for i in range(num_pops):
        S = f"S{i+1} = y[{i * 4}]"
        I = f"I{i+1} = y[{i * 4 + 1}]"
        R = f"R{i+1} = y[{i * 4 + 2}]"
        
        func_ode += f"    {S}\n"
        func_ode += f"    {I}\n"
        func_ode += f"    {R}\n"
    
    for eq in equacoes:
        func_ode += f"    dydt.append({eq})\n"
    
    func_ode += "    return dydt\n"
    
    exec(func_ode, globals())
    return globals()['ode_system']

POPULACOES = [] #criando um vetor para armazenar as populações

'''Criando as populações'''
pop1 = population(10**5, 0, [0.5, 0.2], 0.2, 0.5)

pop2 = population(10**5, 0, [0.5, 0.2], 0.2, 0.5)

POPULACOES.append(pop1) #inserindo as populações criadas no vetor populações
POPULACOES.append(pop2) #TODO: Achar uma maneira melhor de adicionar à POPULACOES

tempo = intervalo_tempo(0, 100)

w = [] #vetor para armazenar as condições iniciais
for i in range(len(POPULACOES)):
    w.extend(POPULACOES[i].condicoes_iniciais()) #adicionando as condições iniciais de cada população

sistema_eq = gerar_ode(len(POPULACOES))
solucoes = odeint(sistema_eq, w, tempo[2], args=(POPULACOES, ))

"""Armazenamento em variáveis dos valores de saída"""
S1 = solucoes[:,0] #pegando o valor do primeiro elemento da lista do sistema de equações
I1 = solucoes[:,1] #pegando o valor do segundo elemento da lista do sistema de equações
R1 = solucoes[:,2] #pegando o valor do terceiro elemento da lista do sistema de equações
Icum1 = solucoes[:,3]

S2 = solucoes[:,4] #pegando o valor do primeiro elemento da lista do sistema de equações
I2 = solucoes[:,5] #pegando o valor do segundo elemento da lista do sistema de equações
R2 = solucoes[:,6] #pegando o valor do terceiro elemento da lista do sistema de equações'
Icum2 = solucoes[:,7]

#IcumTotal = [a + b for a, b in zip(solucoes[:,3], solucoes[:,7])]
IcumTotal = Icum1 + Icum2

"""Armazenamento dos valores"""
df = pd.DataFrame({
    'Suscetiveis 1': S1,
    'infectados 1': I1,
    'Recupearados 1': R1,
    'Suscetiveis 2': S2,
    'infectados 2': I2,
    'Recupearados 2': R2,
    'Infectados Acumulado 1' : Icum1,
    'Infectados Acumulado 2' : Icum2,
})
df.to_csv("./resultados.csv", sep=',')


"""Plotagem do gráfico"""
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
fig.suptitle('Número de infectados')
ax1.plot(tempo[2], I1, 'r', label = 'Infectados população 1')
ax1.plot(tempo[2], I2, 'b', label = 'Infectados população 2')
ax1.set_xlabel('t(dias)')
ax1.set_ylabel('Número de Infectados')
ax1.legend(loc = "upper right")

ax2.plot(tempo[2], Icum1, 'r', label = 'Infectados total na pop 1')
ax2.plot(tempo[2], Icum2, 'b', label = 'Infectados total na pop 2')
ax2.plot(tempo[2], IcumTotal, 'y', label = 'Infectados total')
ax2.set_xlabel('t(dias)')
ax2.set_ylabel('Número de Infectados')
ax2.legend(loc = "upper right")

plt.show()