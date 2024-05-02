"""Importação de bibliotecas para o código"""
import numpy as np
import random
import math

from matplotlib import pyplot as plt


"""Possibilidades para configuração do modelo"""
def visitacao_gaussiana(var):
    """
    Define um padrão de visita guassiana.
    """
    return math.e**(-var**2/2)/math.sqrt(2*math.pi)

def visitacao_CauchyLorentz(var, temperatura):
    """
    Define um padrão de visita com base na probabilidade de Cauchy-Lorentz
    """
    #return 1/(math.pi*(1+var**2))
    return temperatura/(temperatura**2 + var**2)


def resfriamento_fatorMeio(temperatura):
    """
    Reduz a temperatura pela metade
    """
    return temperatura/2

def resfriamento_hiperbolico(temperatura_inicial, iteração):
    """
    Reduz a temperatura de acordo com uma função hiperbólica da iteração
    Para um resfriamento mais rápido utilizar temperatura_inicial/iteração
    """
    return temperatura_inicial/iteração
    #return temperatura_inicial/(1 + iteração)

def resfriamento_geometrico(temperatura_inicial, fator_resfriamento, iteracao):
    """
    Reduz a temperatura de maneira geometrica com base em um fator
    de resfrimento
    """
    return (fator_resfriamento**iteracao)*temperatura_inicial

#TODO: pegar uma equação que possua múltiplos pontos de mínimos globais
def f(x,y):
    """
    Função a ser otimizada
    """
    #return x**2 + y**2 - 6*x - 8*y + 26 #usar intervalor de -5 a 5
    return 4*(x**2 + y**2) - 2*(math.sin(9*x) + math.sin(9*y)) + 3.8 #Usar intervalos de -1 a 1


"""Parâmetros da simulação"""
#limites = np.asarray([[-5, 5]]) #domínio do problema
limites = np.asarray([[-1, 1]])

n_interacoes = 1000 #número de iterações 
#temp_inicial = 2 #temperatura inicial 
temp_inicial = 15
temp_final = 0.008 #temperatura final 
fator_resfriamento = 0.8 #o professor variava de 0.8 a 0.99 

"""Sorteio de uma solução inicial"""
x_inicial = limites[:, 0] + random.random() * (limites[:, 1] - limites[:, 0]) #escolha de um x inicial
y_inicial = limites[:, 0] + random.random() * (limites[:, 1] - limites[:, 0]) #escolha de um i inicial

fx_inicial = f(x_inicial, y_inicial) #valor da função com x e y inicial defeinidos acima


"""Valores atuais de x, y e f(x) à serem substituidos conforme as iterações acontecem"""
x_atual, y_atual = x_inicial, y_inicial
fx_atual = fx_inicial
temp_atual = temp_inicial
melhor_x, melhor_y, melhor_fx = x_atual, y_atual, fx_atual


pontuacoes = [] #lista para armazenar os valores da "energia"
xs, ys = [], [] #listas para armazenar os valores de x e y

#TODO: mudar o critério de parada de uma temperatura final para um número máximo de iterações
"""Começo dos cálculos"""
#while temp_atual >= temp_final: #enquanto a temperatura inicial for maior que a final
for j in range(50): #Realizará o processo de resfriamento 100 vezes
    for i in range(n_interacoes): #enquanto i for menor que o numero de interações

        """Sorteios"""
        #x_i = limites[:, 0] + random.random() * (limites[:, 1] - limites[:, 0]) #sorteio do x
        #y_i = limites[:, 0] + random.random() * (limites[:, 1] - limites[:, 0]) #sorteio do y
        x_i = x_atual + np.random.standard_cauchy() * (limites[:, 1] - limites[:, 0]) #sorteio do x
        y_i = y_atual + np.random.standard_cauchy() * (limites[:, 1] - limites[:, 0]) #sorteio do y
        #x_i = limites[:, 0] + visitacao_CauchyLorentz(x_atual, temp_atual) * (limites[:, 1] - limites[:, 0]) #atualização do x com base no valor atual
        #y_i = limites[:, 0] + visitacao_CauchyLorentz(y_atual, temp_atual) * (limites[:, 1] - limites[:, 0]) #atualização do y com base no valor atual
        #x_i = limites[:, 0] + visitacao_gaussiana(x_atual) * (limites[:, 1] - limites[:, 0])
        #y_i = limites[:, 0] + visitacao_gaussiana(y_atual) * (limites[:, 1] - limites[:, 0])
        pa = random.random() #sorteio de uma probabilidade aleatória

        fx_candidato = f(x_i, y_i) #f(x) calculado a partir dos sorteios candidato a ser a nova solução

        """Condições para aceite do f(x) recém calculado"""
        if fx_atual >= fx_candidato: #se a solução atual for maior que a solução candidata
            fx_atual = fx_candidato
            x_atual, y_atual = x_i, y_i
        else: #caso não seja calcular a probabilidade natural e comparar com a aleatória
            pn = 1/(math.e**((fx_candidato - fx_atual)/temp_atual)) #probabilidade natural do annealing
            if pn >= pa: #se a probabilidade natural for maior ou igual a aleatória aceita-se à candidata
                fx_atual = fx_candidato
                x_atual, y_atual = x_i, y_i

        """Armazenando os valores"""
        pontuacoes.append(fx_atual)
        xs.append(x_atual)
        ys.append(y_atual)
        print(f'Iteração:{i} \tX atual:{x_atual} \tY atual:{y_atual} \tTemperatura: {temp_atual} \tEnergia do Sistema:{fx_atual}')   

        if fx_atual < melhor_fx:
            melhor_fx = fx_atual
            melhor_x = x_i
            melhor_y = y_i


    """Resfriamento"""
    temp_atual = resfriamento_hiperbolico(temp_inicial, j + 1)
    #temp_atual = resfriamento_fatorMeio(temp_atual)
    #temp_atual = resfriamento_geometrico(temp_inicial, fator_resfriamento, j+1) 
    print(f'Temperatura atual do sistema:{temp_atual}')
    print()


"""Solução final encontrada"""
print(f'Solução ótima do sistema: X:{melhor_x}, Y:{melhor_y}, f(x,y): {melhor_fx}')


"""Plotagem do gráfico"""
plt.figure()
plt.suptitle("Evolução dos estados e custos do Simulated Annealing")
plt.plot(pontuacoes, 'r')
plt.title("Valores de Energia")
plt.xlabel("Iterações")
plt.ylabel("Valores de 'Energia'")
plt.show()




